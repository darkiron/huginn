import argparse, os, time, math, json, psutil, torch
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from typing import List, Tuple
from .model import CharRNN
from .tokenizer import CharTokenizer   # legacy/byte fallback
from .tokenizer_bpe import BPETokenizer

# ---------- Datasets ----------
class CharDataset(Dataset):
    def __init__(self, text_ids: List[int], seq_len: int):
        self.data = torch.tensor(text_ids, dtype=torch.long)
        self.seq_len = seq_len
    def __len__(self): return max(0, len(self.data)-self.seq_len-1)
    def __getitem__(self, i):
        x = self.data[i:i+self.seq_len]
        y = self.data[i+1:i+self.seq_len+1]
        return x, y

class MultiCorpus:
    """Holds several id-sequences and samples one uniformly by weight each batch."""
    def __init__(self, corpora_ids: List[List[int]], weights: List[float], seq_len: int):
        self.corpora = [torch.tensor(c, dtype=torch.long) for c in corpora_ids]
        self.seq_len = seq_len
        s = sum(weights)
        self.weights = [w/s for w in weights]
    def sample_batch(self, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor]:
        # choose which corpus for each sample
        choices = torch.multinomial(torch.tensor(self.weights), num_samples=batch_size, replacement=True)
        xs, ys = [], []
        for cidx in choices.tolist():
            data = self.corpora[cidx]
            if len(data) <= self.seq_len + 1:
                # pad with self
                start = 0
            else:
                start = torch.randint(0, len(data)-self.seq_len-1, (1,)).item()
            x = data[start:start+self.seq_len]
            y = data[start+1:start+self.seq_len+1]
            xs.append(x.unsqueeze(0)); ys.append(y.unsqueeze(0))
        return torch.cat(xs, dim=0), torch.cat(ys, dim=0)

# ---------- eval ----------
@torch.no_grad()
def evaluate(model, dl, device):
    model.eval()
    tot, n = 0.0, 0
    for x,y in dl:
        x,y = x.to(device), y.to(device)
        logits,_ = model(x)
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
        tot += loss.item() * x.size(0)
        n += x.size(0)
    return tot / max(1,n)

def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

def main():
    p = argparse.ArgumentParser()
    # data
    p.add_argument("--file", help="(deprecated) single file")
    p.add_argument("--files", nargs="*", help="multiple corpus files")
    p.add_argument("--weights", nargs="*", type=float, help="sampling weights per file")
    p.add_argument("--seq-len", type=int, default=128)
    # tokenizer
    p.add_argument("--tokenizer", choices=["bpe","byte","legacy"], default="bpe")
    p.add_argument("--vocab-size", type=int, default=8000)
    # model
    p.add_argument("--emb", type=int, default=256)
    p.add_argument("--hid", type=int, default=512)
    p.add_argument("--layers", type=int, default=2)
    p.add_argument("--dropout", type=float, default=0.1)
    # train
    p.add_argument("--lr", type=float, default=3e-3)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--epochs", type=int, default=10)
    # io
    p.add_argument("--ckpt", default="/ckpts/rnn.pt")
    p.add_argument("--metrics-dir", default="/data/metrics")  # logs éco-index
    args = p.parse_args()

    os.makedirs(os.path.dirname(args.ckpt), exist_ok=True)
    os.makedirs(args.metrics_dir, exist_ok=True)

    # --------- load data texts ---------
    texts: List[str] = []
    if args.files and len(args.files) > 0:
        for f in args.files:
            with open(f, "r", encoding="utf-8") as fh:
                texts.append(fh.read())
        weights = args.weights if args.weights else [1.0]*len(texts)
        if len(weights) != len(texts):
            raise ValueError("--weights must match --files length")
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            texts = [fh.read()]
        weights = [1.0]
    else:
        raise ValueError("Provide --files ... (preferred) or --file ...")

    # --------- build / load tokenizer ---------
    special_tokens = ["<|prompt|>", "<|endprompt|>", "<|answer|>", "<|endanswer|>"]
    tok_type = args.tokenizer

    if tok_type == "bpe":
        # Train BPE on all texts combined
        tokenizer = BPETokenizer.train(texts, vocab_size=args.vocab_size, specials=special_tokens)
        tokenizer_payload = {"kind":"bpe","data": tokenizer.to_json()}
        def encode_text(t: str) -> List[int]: return tokenizer.encode(t)
        vocab_size = tokenizer.size()
    elif tok_type == "byte":
        # reuse CharTokenizer in byte mode (it already supports byte-level)
        tok = CharTokenizer(None)  # byte mode
        tokenizer_payload = {"kind":"byte","data": None}
        def encode_text(t: str) -> List[int]: return tok.encode(t)
        vocab_size = 256
    else:
        # legacy char-level (NOT recommended)
        tok = CharTokenizer()
        tokenizer_payload = {"kind":"legacy","data": None}
        def encode_text(t: str) -> List[int]: return tok.encode(t)
        vocab_size = len(tok.chars)

    corpora_ids = [ encode_text(t) for t in texts ]

    # train/val split for the FIRST corpus (simple; adequate for early signal)
    full_ids = corpora_ids[0]
    split = int(0.95*len(full_ids))
    train_ids = full_ids[:split]; val_ids = full_ids[split:]
    train_ds = CharDataset(train_ids, args.seq_len)
    val_ds   = CharDataset(val_ids,   args.seq_len)

    dl_val = DataLoader(val_ds, batch_size=args.batch, shuffle=False, drop_last=False)

    # multi-corpus sampler for the training loop
    multi = MultiCorpus(corpora_ids, weights, args.seq_len)

    device = "cpu"
    model = CharRNN(vocab_size=vocab_size, emb=args.emb, hid=args.hid, layers=args.layers, dropout=args.dropout).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)

    # --------- resource logging setup ---------
    proc = psutil.Process(os.getpid())
    last_times = proc.cpu_times()
    max_rss = 0
    started = time.time()
    # Approx count of tokens shown to the model
    tokens_seen = 0

    # --------- train loop ---------
    steps_per_epoch = 500  # fixed budget; keeps epochs time-bounded across corpora
    for epoch in range(1, args.epochs+1):
        model.train()
        t0 = time.time()
        for step in range(steps_per_epoch):
            x,y = multi.sample_batch(args.batch)
            tokens_seen += x.numel()
            x,y = x.to(device), y.to(device)
            logits,_ = model(x)
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            # track max RSS
            mem = proc.memory_info().rss
            if mem > max_rss: max_rss = mem

        # validation
        val_loss = evaluate(model, dl_val, device)
        print(f"epoch {epoch}/{args.epochs} val_loss={val_loss:.4f}")

        # save BEST ckpt by val_loss
        ckpt = {
            "state_dict": model.state_dict(),
            "tokenizer": tokenizer_payload,
            "config": {"emb": args.emb, "hid": args.hid, "layers": args.layers, "dropout": args.dropout,
                       "vocab_size": vocab_size, "tokenizer_kind": tok_type},
        }
        torch.save(ckpt, args.ckpt)

        # epoch resource log
        now = time.time()
        cur_times = proc.cpu_times()
        epoch_log = {
            "ts": _now_iso(),
            "epoch": epoch,
            "val_loss": float(val_loss),
            "wall_sec_epoch": now - t0,
            "wall_sec_total": now - started,
            "cpu_user_sec_epoch": cur_times.user - last_times.user,
            "cpu_sys_sec_epoch": cur_times.system - last_times.system,
            "rss_bytes_max_so_far": int(max_rss),
            "tokens_seen": int(tokens_seen),
            "batch_size": args.batch,
            "seq_len": args.seq_len,
            "vocab_size": vocab_size,
        }
        last_times = cur_times

        # append JSONL
        os.makedirs(args.metrics_dir, exist_ok=True)
        with open(os.path.join(args.metrics_dir, "train_metrics.jsonl"), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(epoch_log) + "\n")

if __name__ == "__main__":
    main()
