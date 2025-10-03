# Byte-level & legacy char-level compatible tokenizer
# - Par défaut: byte-level (0..255) -> préserve accents/UTF-8
# - Compatible anciens ckpts: si `chars` est une liste de str, on bascule en mode legacy

from __future__ import annotations
from typing import List, Optional, Union

class CharTokenizer:
    """
    Byte-level tokenizer par défaut.
    - mode="byte": encode() -> liste d'octets (ints 0..255), decode() -> UTF-8 (errors='replace')
    - mode="legacy": compat char-level si ckpt ancien (chars=list[str])
    """
    def __init__(self, chars: Optional[List[Union[int, str]]] = None):
        # Si aucun vocab fourni -> byte-level
        if chars is None:
            self.mode = "byte"
            self.chars = list(range(256))  # vocab fixe
            # stoi/itos inutiles en byte-level, mais on garde API uniforme
            self.stoi = {i: i for i in range(256)}
            self.itos = {i: i for i in range(256)}
            return

        # Détection du mode selon le type des éléments du ckpt
        if all(isinstance(c, int) for c in chars):
            # On considère que c'est un ckpt byte-level (0..255)
            self.mode = "byte"
            self.chars = list(range(256))
            self.stoi = {i: i for i in range(256)}
            self.itos = {i: i for i in range(256)}
        elif all(isinstance(c, str) for c in chars):
            # Legacy char-level (liste de caractères)
            self.mode = "legacy"
            self.chars = list(chars)
            self.stoi = {c: i for i, c in enumerate(self.chars)}
            self.itos = {i: c for i, c in enumerate(self.chars)}
        else:
            # Cas mixte improbable -> fallback byte-level
            self.mode = "byte"
            self.chars = list(range(256))
            self.stoi = {i: i for i in range(256)}
            self.itos = {i: i for i in range(256)}

    def encode(self, s: str) -> List[int]:
        """
        Convertit une chaîne en indices.
        - byte-level: UTF-8 -> bytes -> liste d'int 0..255
        - legacy: mappe char par char, inconnu -> '?'
        """
        if self.mode == "byte":
            b = s.encode("utf-8", errors="replace")
            return list(b)
        # legacy
        out = []
        qidx = self.stoi.get("?", None)
        for ch in s:
            if ch in self.stoi:
                out.append(self.stoi[ch])
            elif qidx is not None:
                out.append(qidx)
            else:
                # Si pas de '?', mappe sur 0
                out.append(0)
        return out

    def decode(self, idxs: List[int]) -> str:
        """
        Convertit des indices en chaîne.
        - byte-level: bytes(idxs).decode('utf-8', errors='replace')
        - legacy: join par itos
        """
        if self.mode == "byte":
            try:
                return bytes(int(i) & 0xFF for i in idxs).decode("utf-8", errors="replace")
            except Exception:
                # fallback très défensif
                return "".join(chr(int(i) & 0xFF) for i in idxs)
        # legacy
        return "".join(self.itos.get(int(i), "?") for i in idxs)

    # Helpers optionnels si tu veux sérialiser proprement le vocab
    def to_serializable(self) -> List[Union[int, str]]:
        """
        Ce que tu mets dans le ckpt (train.py le fait déjà avec `chars`).
        - byte-level: retourne range(256) pour clarté/repro.
        - legacy: retourne la liste de caractères.
        """
        return list(range(256)) if self.mode == "byte" else list(self.chars)
