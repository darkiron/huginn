# LLM Service (Python) 🧠

Notes sur le service LLM Python. Pour les détails approfondis, consulter aussi: ../../docs/services/python-llm.md

## Rôle
- Fournit des capacités de génération de texte (consommées par le backend Symfony).
- Expose des métriques Prometheus pour l'observabilité.
- S'exécute en local via Docker Compose pour une cohérence d'environnement.

## API HTTP attendue par le backend
- Endpoint: `POST /generate/stream`
- URL par défaut côté backend: `http://llm:8008/generate/stream`
  - Configurable via `LLM_URL` (compose/env) ou paramètre Symfony `llm_url`.
- Client côté Symfony: `apps/symfony-back/src/Infrastructure/LLM/PythonLLMClient.php`
  - Utilise le streaming (HttpClientInterface avec `buffer: false`).

Remarque: l'implémentation HTTP de l'endpoint n'est pas incluse dans les extraits visibles ici; assurez-vous que le service LLM répond bien sur ce chemin si utilisé en production.

## CLI — Génération rapide
- Voir [LLM RNN CLI](LLM-RNN-CLI) pour générer du texte directement dans le conteneur `llm`.
- Entrée: `python -m llm_rnn.generate` avec options `--ckpt`, `--seed`, `--chars`, `--temp`, `--top-k`, `--top-p`.

## Tokenization
- Modes pris en charge: byte-level (par défaut), legacy char-level, BPE.
- Détails: [Tokenization](Tokenization) (modes, heuristiques, encode/decode).

## Métriques Prometheus
- Exposées par `services/llm/metrics_server.py` sur `/metrics`.
- Port par défaut: `METRICS_PORT=9108` (voir compose.yaml -> service `llm`).
- Exemple local: http://localhost:9108/metrics

## Supervisor (processus)
- Fichier: `services/llm/supervisor.py`
  - Lance le serveur de métriques dans un thread.
  - Maintient le conteneur vivant via une boucle idle.
- Commande compose: `python services/llm/supervisor.py`

## Répertoire modèle & checkpoints
- Volume: `./ckpts` (hôte) monté en `/ckpts` (conteneur).
- Chemin par défaut du checkpoint: `/ckpts/rnn.pt` (configurable via `CKPT_PATH`).

## Fichiers clés (apps/python-llm)
- `llm_rnn/generate.py` — CLI de génération (charge le ckpt, choisit le tokenizer, échantillonne via le modèle).
- `llm_rnn/model.py` — définition du modèle `CharRNN` et logique de sampling.
- `llm_rnn/tokenizer.py` — tokenizer byte/legacy.
- `llm_rnn/tokenizer_bpe.py` — tokenizer BPE (si ckpt entraîné avec BPE).

Voir aussi:
- [LLM RNN CLI](LLM-RNN-CLI)
- [Backend-Symfony](Backend-Symfony)
- [Architecture](Architecture)
