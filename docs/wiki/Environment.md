# Environment 🔑

Variables d'environnement et configuration. Pour le détail complet, voir ../env.md.

## Backend (Symfony)
- LLM_URL: URL de génération/stream attendue (défaut: http://llm:8008/generate/stream)
- LLM_METRICS_URL: URL des métriques du service LLM (ex.: http://llm:9108/metrics)

Ces valeurs peuvent être définies via:
- Paramètres Symfony (parameters.yaml) et/ou
- Variables d'environnement (voir compose.yaml -> service symfony-back)

## Service LLM (Python)
- CKPT_PATH: chemin du checkpoint (ex.: /ckpts/rnn.pt)
- METRICS_PORT: port d'exposition des métriques (défaut: 9108)
- PYTHONPATH: inclut /app/apps/python-llm pour la CLI et les modules

## Docker Compose (extraits utiles)
Voir compose.yaml:
- Volumes: ./ckpts:/ckpts, ./data:/data, ./apps/python-llm:/app/apps/python-llm
- Ports: 80->java gateway, 8081->laravel-front, 8082->symfony-back, 9108->llm metrics

Voir aussi:
- [Setup](Setup) — démarrage rapide 🐳
- [LLM-Service-Python](LLM-Service-Python) — détails service et API 🧠