from __future__ import annotations
import argparse, os, sys, json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from .model import CharRNN

class CharDataset(Dataset):
    def __init__(self, text: str, seq_len: int = 128):
        self.chars = sorted(set(text))
        self.stoi = {c:i for i,c in enumerate(self.chars)}
        self.itos = {i:c for c,i in self.stoi.items()}
        self.data = [self.stoi[c] for c in text]
        self.seq_len = seq_len

    def __len__(self):
        return max(0, len(self.data) - self.seq_len)

    def __getitem__(self, i):
        x = torch.tensor(self.data[i:i+self.seq_len], dtype=torch.long)
        y = torch.tensor(self.data[i+1:i+self.seq_len+1], dtype=torch.long)
        return x, y

def main():
    p = argparse.ArgumentParser(description="Train tiny char-RNN (CPU)")
    p.add_argument("--file", type=str, help="training file")
    p.add_argument("--train", type=str, help="training text (inline)")
    p.add_argument("--seq-len", type=int, default=128)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--epochs", type=int, default=5)
    p.add_argument("--lr", type=float, default=2e-3)
    p.add_argument("--emb", type=int, default=128)
    p.add_argument("--hid", type=int, default=256)
    p.add_argument("--layers", type=int, default=2)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--ckpt", type=str, default="rnn.pt")
    args = p.parse_args()

    if args.file:
        text = open(args.file, "r", encoding="utf-8").read()
    elif args.train:
        text = args.train
    else:
        print("Paste training text, end with EOF (Ctrl+D / Ctrl+Z):")
        text = sys.stdin.read()

    if not text.strip():
        print("No training text.", file=sys.stderr)
        return 1

    ds = CharDataset(text, seq_len=args.seq_len)
    if len(ds) == 0:
        print("Text too short for seq-len.", file=sys.stderr)
        return 1

    dl = DataLoader(ds, batch_size=args.batch, shuffle=True, drop_last=True)
    model = CharRNN(vocab_size=len(ds.chars), emb=args.emb, hid=args.hid, layers=args.layers, dropout=args.dropout)
    device = torch.device("cpu")
    model.to(device)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    loss_fn = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(1, args.epochs+1):
        total = n = 0.0, 0
        total = 0.0
        n = 0
        for x,y in dl:
            x,y = x.to(device), y.to(device)
            opt.zero_grad()
            logits, _ = model(x)
            loss = loss_fn(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
            loss.backward()
            opt.step()
            total += float(loss.item()); n += 1
        print(f"[epoch {epoch}] loss={total/n:.4f}")

    ckpt = {
        "state_dict": model.state_dict(),
        "chars": ds.chars,
        "config": {"emb": args.emb, "hid": args.hid, "layers": args.layers, "dropout": args.dropout}
    }
    torch.save(ckpt, args.ckpt)
    print(f"Saved -> {args.ckpt} (vocab={len(ds.chars)})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
