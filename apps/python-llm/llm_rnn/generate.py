import argparse, torch, os, sys
sys.path.append(".")
from .tokenizer import CharTokenizer
from .model import CharRNN, sample

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", default="/ckpts/rnn.pt")
    p.add_argument("--seed", default="")
    p.add_argument("--chars", type=int, default=200)
    p.add_argument("--temp", type=float, default=0.9)
    p.add_argument("--top-k", type=int, default=None)
    p.add_argument("--top-p", type=float, default=None)
    args = p.parse_args()

    obj = torch.load(args.ckpt, map_location="cpu")
    tok = CharTokenizer(obj["chars"])
    cfg = obj["config"]
    model = CharRNN(vocab_size=len(tok.chars), emb=cfg["emb"], hid=cfg["hid"], layers=cfg["layers"], dropout=cfg["dropout"])
    model.load_state_dict(obj["state_dict"])
    model.eval()

    seed_idx = tok.encode(args.seed)
    out_idx = sample(model, seed_idx, steps=args.chars, temperature=args.temp, top_k=args.top_k, top_p=args.top_p)
    print(tok.decode(out_idx))

if __name__ == "__main__":
    main()
