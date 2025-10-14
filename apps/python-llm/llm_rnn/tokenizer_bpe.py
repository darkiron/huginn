# Minimal BPE tokenizer (from scratch).
# - whitespace pretokenization
# - learns merges up to vocab_size
# - serializable to { "type": "bpe", "vocab": {...}, "merges": [[a,b], ...] }
# - UTF-8 safe

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Iterable, Optional
import json
import re

_ws_re = re.compile(r"\s+")

def _split_ws(text: str) -> List[str]:
    # keep single spaces as tokens between words
    parts: List[str] = []
    i = 0
    for m in _ws_re.finditer(text):
        if m.start() > i:
            parts.append(text[i:m.start()])
        parts.append(m.group(0))  # the whitespace chunk
        i = m.end()
    if i < len(text):
        parts.append(text[i:])
    return [p for p in parts if p != ""]

def _word_to_symbols(w: str) -> Tuple[str, ...]:
    # char-level initialization (UTF-8 characters)
    return tuple(list(w))

def _get_stats(words: List[Tuple[str, ...]]) -> Dict[Tuple[str, str], int]:
    stats: Dict[Tuple[str, str], int] = {}
    for w in words:
        for i in range(len(w) - 1):
            pair = (w[i], w[i+1])
            stats[pair] = stats.get(pair, 0) + 1
    return stats

def _merge_pair(words: List[Tuple[str, ...]], pair: Tuple[str, str], merged_sym: str) -> List[Tuple[str, ...]]:
    a, b = pair
    out: List[Tuple[str, ...]] = []
    for w in words:
        i = 0
        neww: List[str] = []
        while i < len(w):
            if i < len(w) - 1 and w[i] == a and w[i+1] == b:
                neww.append(merged_sym)
                i += 2
            else:
                neww.append(w[i])
                i += 1
        out.append(tuple(neww))
    return out

@dataclass
class BPETokenizer:
    vocab: Dict[str, int]             # token -> id
    inv_vocab: List[str]              # id -> token
    merges: List[Tuple[str, str]]     # merge rules (a,b) -> a+b
    special: Dict[str, int]           # special tokens (optional)

    # ======== training ========
    @staticmethod
    def train(corpus_texts: Iterable[str], vocab_size: int = 8000, specials: Optional[List[str]] = None) -> "BPETokenizer":
        specials = specials or []
        # Pre-tokenize on whitespace to reduce cross-word merges
        tokens: List[str] = []
        for txt in corpus_texts:
            tokens.extend(_split_ws(txt))

        # words as list of symbol tuples (char-level init)
        words = [ _word_to_symbols(t) for t in tokens ]

        # init vocab with all single chars present + whitespace chunks
        sym_freq: Dict[str, int] = {}
        for w in words:
            for s in w:
                sym_freq[s] = sym_freq.get(s, 0) + 1

        vocab: Dict[str, int] = {}
        inv_vocab: List[str] = []
        for s in specials:
            if s not in vocab:
                vocab[s] = len(inv_vocab); inv_vocab.append(s)
        for s in sorted(sym_freq.keys()):
            if s not in vocab:
                vocab[s] = len(inv_vocab); inv_vocab.append(s)

        merges: List[Tuple[str, str]] = []
        # keep merging most frequent pairs until reaching vocab_size
        while len(inv_vocab) < vocab_size:
            stats = _get_stats(words)
            if not stats:
                break
            best_pair, cnt = max(stats.items(), key=lambda x: x[1])
            if cnt < 2:
                break
            a, b = best_pair
            merged_sym = a + b
            merges.append((a, b))
            words = _merge_pair(words, best_pair, merged_sym)
            if merged_sym not in vocab:
                vocab[merged_sym] = len(inv_vocab); inv_vocab.append(merged_sym)

        return BPETokenizer(vocab=vocab, inv_vocab=inv_vocab, merges=merges,
                            special={s: vocab[s] for s in specials})

    # ======== serialization ========
    def to_json(self) -> str:
        obj = {
            "type": "bpe",
            "vocab": self.vocab,
            "inv_vocab": self.inv_vocab,   # store for exact roundtrip
            "merges": self.merges,
            "special": self.special,
        }
        return json.dumps(obj, ensure_ascii=False)

    @staticmethod
    def from_json(s: str) -> "BPETokenizer":
        obj = json.loads(s)
        if obj.get("type") != "bpe":
            raise ValueError("Not a BPE tokenizer payload")
        return BPETokenizer(
            vocab=obj["vocab"],
            inv_vocab=obj["inv_vocab"],
            merges=[tuple(x) for x in obj["merges"]],
            special=obj.get("special", {})
        )

    # ======== encoding/decoding ========
    def encode(self, text: str) -> List[int]:
        ids: List[int] = []
        for token in _split_ws(text):
            # start from char symbols
            syms: List[str] = list(_word_to_symbols(token))
            # apply merges greedily in learned order
            for a, b in self.merges:
                i = 0
                merged: List[str] = []
                while i < len(syms):
                    if i < len(syms) - 1 and syms[i] == a and syms[i+1] == b:
                        merged.append(a+b)
                        i += 2
                    else:
                        merged.append(syms[i])
                        i += 1
                syms = merged
                if len(syms) == 1:
                    # cannot merge further
                    pass
            for s in syms:
                tok_id = self.vocab.get(s)
                if tok_id is None:
                    # unknown piece fallback: decompose to chars
                    for ch in s:
                        cid = self.vocab.get(ch, None)
                        if cid is not None:
                            ids.append(cid)
                        else:
                            # last resort: skip
                            pass
                else:
                    ids.append(tok_id)
        return ids

    def decode(self, ids: List[int]) -> str:
        pieces = [ self.inv_vocab[i] if 0 <= i < len(self.inv_vocab) else "" for i in ids ]
        return "".join(pieces)

    # ======== helpers ========
    def size(self) -> int:
        return len(self.inv_vocab)
