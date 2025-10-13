import argparse, os, math, torch
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from .config import TrainConfig
from .tokenizer import CharTokenizer
from .model import CharRNN

class CharDataset(Dataset):
    def __init__(self, text:str, tok:CharTokenizer, seq_len:int):
        self.tok = tok
        self.seq_len = seq_len
        self.data = torch.tensor(tok.encode(text), dtype=torch.long)
    def __len__(self): return max(0, len(self.data)-self.seq_len-1)
    def __getitem__(self, i):
        x = self.data[i:i+self.seq_len]
        y = self.data[i+1:i+self.seq_len+1]
        return x, y

def evaluate(model, dl, device):
    model.eval()
    tot, n = 0.0, 0
    with torch.no_grad():
        for x,y in dl:
            x,y = x.to(device), y.to(device)
            logits,_ = model(x)
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
            tot += loss.item() * x.size(0)
            n += x.size(0)
    return tot / max(1,n)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    p.add_argument("--ckpt", default="/ckpts/rnn.pt")
    p.add_argument("--emb", type=int, default=128)
    p.add_argument("--hid", type=int, default=256)
    p.add_argument("--layers", type=int, default=2)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--lr", type=float, default=3e-3)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--seq-len", type=int, default=128)
    p.add_argument("--epochs", type=int, default=5)
    args = p.parse_args()

    torch.manual_seed(1337)
    device = "cpu"

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    tok = CharTokenizer()
    ds = CharDataset(text, tok, args.seq_len)
    n = int(len(ds) * 0.95)
    train_ds, val_ds = torch.utils.data.random_split(ds, [n, len(ds)-n])

    dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, drop_last=True)
    dl_val = DataLoader(val_ds, batch_size=args.batch, shuffle=False, drop_last=False)

    model = CharRNN(vocab_size=len(tok.chars), emb=args.emb, hid=args.hid, layers=args.layers, dropout=args.dropout).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)

    best_val = float("inf")
    for epoch in range(1, args.epochs+1):
        model.train()
        for x,y in dl:
            x,y = x.to(device), y.to(device)
            logits,_ = model(x)
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
        val = evaluate(model, dl_val, device)
        print(f"epoch {epoch}/{args.epochs} val_loss={val:.4f}")
        if val < best_val:
            best_val = val
            ckpt = {
              "state_dict": model.state_dict(),
              "chars": tok.chars,
              "config": {"emb": args.emb, "hid": args.hid, "layers": args.layers, "dropout": args.dropout}
            }
            os.makedirs(os.path.dirname(args.ckpt), exist_ok=True)
            torch.save(ckpt, args.ckpt)
            print(f"saved best ckpt -> {args.ckpt} (val_loss={val:.4f})")

if __name__ == "__main__":
    main()
