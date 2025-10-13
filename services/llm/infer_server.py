from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os
import torch

# Chemins / imports du package
import sys
sys.path.append("/app/apps/python-llm")
from llm_rnn.model import CharRNN, sample
from llm_rnn.tokenizer import CharTokenizer

CKPT = os.getenv("CKPT_PATH", "/ckpts/rnn.pt")
DEVICE = "cpu"

class LLM:
    def __init__(self, ckpt_path:str):
        obj = torch.load(ckpt_path, map_location=DEVICE)
        cfg = obj["config"]
        self.tok = CharTokenizer(obj["chars"])
        self.model = CharRNN(vocab_size=len(self.tok.chars), emb=cfg["emb"], hid=cfg["hid"], layers=cfg["layers"], dropout=cfg["dropout"])
        self.model.load_state_dict(obj["state_dict"])
        self.model.to(DEVICE).eval()
    def generate(self, seed:str, max_new:int, temp:float=0.9, top_k=None, top_p=None):
        seed_idx = self.tok.encode(seed)
        out_idx = sample(self.model, seed_idx, steps=max_new, temperature=temp, top_k=top_k, top_p=top_p)
        return self.tok.decode(out_idx)

llm = None

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/generate":
            self.send_response(404); self.end_headers(); return
        length = int(self.headers.get("Content-Length","0"))
        data = json.loads(self.rfile.read(length) or "{}")
        seed = data.get("seed","")
        temp = float(data.get("temperature", 0.9))
        max_new = int(data.get("max_new_tokens", 200))
        top_k = data.get("top_k")
        top_p = data.get("top_p")
        global llm
        if llm is None:
            if not os.path.exists(CKPT):
                self.send_response(500); self.end_headers(); self.wfile.write(b'{"error":"ckpt not found"}'); return
            llm = LLM(CKPT)
        text = llm.generate(seed, max_new, temp, top_k, top_p)
        out = json.dumps({"text": text}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

def run(port:int=8008):
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

if __name__ == "__main__":
    run(int(os.getenv("INFER_PORT","8008")))
