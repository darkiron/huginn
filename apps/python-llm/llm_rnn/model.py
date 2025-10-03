import torch, torch.nn as nn

class CharRNN(nn.Module):
    def __init__(self, vocab_size:int, emb:int=128, hid:int=256, layers:int=2, dropout:float=0.1):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, emb)
        self.rnn = nn.LSTM(emb, hid, num_layers=layers, batch_first=True, dropout=dropout)
        self.head = nn.Linear(hid, vocab_size)
    def forward(self, x, h=None):
        x = self.emb(x)
        y, h = self.rnn(x, h)
        logits = self.head(y)
        return logits, h

@torch.no_grad()
def sample(model:CharRNN, seed_idxs, steps:int, temperature:float=1.0, top_k:int|None=None, top_p:float|None=None):
    device = next(model.parameters()).device
    idxs = torch.tensor(seed_idxs, dtype=torch.long, device=device).unsqueeze(0)
    h = None
    out = idxs.clone()
    for _ in range(steps):
        logits, h = model(out[:, -1:], h)
        logits = logits[:, -1, :] / max(1e-6, temperature)
        probs = torch.softmax(logits, dim=-1)

        if top_k is not None:
            v, ix = torch.topk(probs, k=top_k, dim=-1)
            mask = torch.zeros_like(probs)
            mask.scatter_(1, ix, v)
            probs = mask / mask.sum(dim=-1, keepdim=True)
        if top_p is not None:
            sp, si = torch.sort(probs, descending=True, dim=-1)
            cdf = torch.cumsum(sp, dim=-1)
            keep = (cdf <= top_p).float()
            # Toujours garder au moins le 1er token
            keep[:,0] = 1.0
            filtered = sp * keep
            filtered = filtered / filtered.sum(dim=-1, keepdim=True)
            probs = torch.zeros_like(probs).scatter(1, si, filtered)

        nxt = torch.multinomial(probs, num_samples=1)
        out = torch.cat([out, nxt], dim=1)
    return out.squeeze(0).tolist()
