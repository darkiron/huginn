from __future__ import annotations
import torch
import torch.nn as nn

class CharRNN(nn.Module):
    def __init__(self, vocab_size: int, emb: int = 128, hid: int = 256, layers: int = 2, dropout: float = 0.1):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, emb)
        self.rnn = nn.LSTM(emb, hid, num_layers=layers, batch_first=True, dropout=dropout)
        self.head = nn.Linear(hid, vocab_size)

    def forward(self, x, h=None):
        x = self.emb(x)               # [B, T, emb]
        y, h = self.rnn(x, h)         # y: [B, T, hid]
        logits = self.head(y)         # [B, T, V]
        return logits, h

def sample(model: CharRNN, seed_idxs, steps: int, temperature: float = 1.0):
    model.eval()
    device = next(model.parameters()).device
    import torch
    idxs = torch.tensor(seed_idxs, dtype=torch.long, device=device).unsqueeze(0)  # [1, T]
    h = None
    out = idxs.clone()
    with torch.no_grad():
        for _ in range(steps):
            logits, h = model(out[:, -1:].to(device), h)  # autoreg step by step
            logits = logits[:, -1, :] / max(1e-6, temperature)
            probs = torch.softmax(logits, dim=-1)
            nxt = torch.multinomial(probs, num_samples=1)  # [1,1]
            out = torch.cat([out, nxt], dim=1)
    return out.squeeze(0).tolist()
