# Setup ⚙️🐳

Cette page résume l'installation locale et renvoie vers la source de vérité détaillée.

- Guide complet: ../setup.md

## Démarrage rapide
- Prérequis: Docker Desktop 4.x+
- Depuis la racine du dépôt:
  - Copier/configurer les fichiers d'environnement selon ../env.md
  - Lancer: `docker compose up -d`

## Services exposés (par défaut)
- Frontend (Laravel): http://localhost:8081 (la page d'accueil peut aussi être servie via le gateway: http://localhost:80)
- Backend (Symfony): http://localhost:8082
- LLM (metrics): http://localhost:9108/metrics

Voir aussi:
- [Architecture](Architecture) — panorama et flux 🗺️
- [Environment](Environment) — variables d'environnement 🔑
- [LLM RNN CLI](LLM-RNN-CLI) — génération locale via Docker 🧠