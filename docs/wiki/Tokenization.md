# Tokenization 🔤

Aperçu des stratégies de tokenisation utilisées par le service LLM Python. Source code: apps/python-llm/llm_rnn.

## Modes pris en charge
- Byte-level (par défaut) — 0..255
  - Préserve les accents/UTF‑8 via encodage/décodage bytes.
  - Implémentation: `llm_rnn/tokenizer.py` (`CharTokenizer` avec `mode="byte"`).
- Legacy char-level — liste de caractères
  - Pour compat CKPT anciens; mappe chaque char à un indice.
  - Hors vocabulaire: `?` si présent, sinon fallback 0.
- BPE — (si le checkpoint est entraîné avec BPE)
  - Implémentation: `llm_rnn/tokenizer_bpe.py` (requis par `tokenizer_kind="bpe"`).

## Détection du mode
- Dans `llm_rnn/generate.py`: le checkpoint charge `config["tokenizer_kind"]` ("bpe" | "byte" | "legacy").
- Sinon, heuristique via `chars`:
  - ints -> byte-level
  - str -> legacy char-level

## API encode/decode
- encode(str) -> List[int]
  - byte-level: UTF‑8 -> bytes -> liste 0..255 (errors='replace')
  - legacy: conversion char->id avec fallback `?`/0
- decode(List[int]) -> str
  - byte-level: bytes(...).decode('utf-8', errors='replace')
  - legacy: join via itos avec fallback `?`

## Bonnes pratiques
- Vérifier la compatibilité entre le checkpoint et la tokenizer (kind, vocab).
- En cas d'artefacts de décodage, baisser la température (`--temp`) et confirmer le mode.

Voir aussi:
- [LLM RNN CLI](LLM-RNN-CLI)
- [LLM-Service-Python](LLM-Service-Python)