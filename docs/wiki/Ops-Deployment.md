# Ops & Deployment 🚀

Notes d'exploitation et de déploiement. Pour le guide complet, voir ../ops/deployment.md.

## Services (compose.yaml)
- java-gateway (port 80 -> 8080)
- laravel-front (port 8081 -> 8080)
- symfony-back (port 8082 -> 8080)
- llm (metrics 9108 -> 9108)

Volumes clés:
- ./apps/laravel-front -> /var/www/html
- ./apps/symfony-back -> /app
- ./apps/python-llm -> /app/apps/python-llm
- ./ckpts -> /ckpts
- ./data -> /data

Env importants:
- LLM_URL, LLM_METRICS_URL côté backend
- CKPT_PATH, METRICS_PORT, PYTHONPATH côté LLM

Observabilité:
- Prometheus peut scrapper le LLM sur http://llm:9108/metrics (ou via l’hôte: http://localhost:9108/metrics)

Voir aussi:
- [Architecture](Architecture) 🗺️
- [LLM-Service-Python](LLM-Service-Python) 🧠