import argparse, torch, json
from .model import CharRNN
from .tokenizer import CharTokenizer
from .tokenizer_bpe import BPETokenizer

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
    cfg = obj["config"]
    kind = cfg.get("tokenizer_kind", "legacy")
    # load tokenizer
    if kind == "bpe":
        payload = obj["tokenizer"]["data"]
        tok = BPETokenizer.from_json(payload)
        vocab_size = tok.size()
        def encode(s): return tok.encode(s)
        def decode(ix): return tok.decode(ix)
    elif kind == "byte":
        tok = CharTokenizer(None)
        vocab_size = 256
        encode = tok.encode; decode = tok.decode
    else:
        tok = CharTokenizer()
        vocab_size = len(tok.chars)
        encode = tok.encode; decode = tok.decode

    model = CharRNN(vocab_size=vocab_size, emb=cfg["emb"], hid=cfg["hid"], layers=cfg["layers"], dropout=cfg["dropout"])
    model.load_state_dict(obj["state_dict"]); model.eval()

    from .model import sample
    seed_idx = encode(args.seed)
    out_idx = sample(model, seed_idx, steps=args.chars, temperature=args.temp, top_k=args.top_k, top_p=args.top_p)
    print(decode(out_idx))

if __name__ == "__main__":
    main()
