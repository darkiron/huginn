from __future__ import annotations
import argparse, torch
from .model import CharRNN, sample

def main():
    p = argparse.ArgumentParser(description="Generate from tiny char-RNN")
    p.add_argument("--ckpt", type=str, default="rnn.pt")
    p.add_argument("--seed", type=str, default=" ")
    p.add_argument("--chars", type=int, default=400)
    p.add_argument("--temp", type=float, default=0.9)
    args = p.parse_args()

    ckpt = torch.load(args.ckpt, map_location="cpu")
    chars = ckpt["chars"]; stoi = {c:i for i,c in enumerate(chars)}; itos = {i:c for c,i in stoi.items()}
    cfg = ckpt["config"]
    model = CharRNN(vocab_size=len(chars), **cfg)
    model.load_state_dict(ckpt["state_dict"])
    model.eval()

    seed_idxs = [stoi.get(c, 0) for c in args.seed]
    out_idxs = sample(model, seed_idxs, steps=args.chars, temperature=args.temp)
    text = "".join(itos.get(i, "?") for i in out_idxs)
    print(text)

if __name__ == "__main__":
    raise SystemExit(main())
