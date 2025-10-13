from dataclasses import dataclass

@dataclass
class TrainConfig:
    emb:int=128
    hid:int=256
    layers:int=2
    dropout:float=0.1
    lr:float=3e-3
    batch:int=64
    seq_len:int=128
    epochs:int=5
