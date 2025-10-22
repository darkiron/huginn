# Huginn ✨

Welcome! Huginn is a multi‑service AI application designed for a smooth dev experience and clear boundaries between services. 🙌

What’s inside:
- 🧱 Symfony backend (apps/symfony-back)
- 🌐 Laravel frontend (apps/laravel-front)
- 🧠 Python LLM service (apps/python-llm)

This repository is structured as a monorepo and includes a Docker Compose setup for local development.

## Quick links 🔗
- 📚 Documentation index: docs/README.md
- 🗂️ GitHub Wiki source (to copy into your repo wiki): docs/wiki/Home.md

## Getting started (Docker) 🐳
1. Prérequis : Docker Desktop 4.x ou plus récent.
2. Depuis la racine du dépôt :
   - Copiez ou créez les fichiers d’environnement comme décrit dans docs/env.md.
   - Démarrez la stack : `docker compose up -d`
3. Ouvrez les services (valeurs par défaut) :
   - 🖥️ Frontend : http://localhost:8080 (ajustez si votre compose utilise un autre port)
   - 🔙 Backend API : http://localhost:8000
   - 🧪 Python LLM : http://localhost:9000 ou selon compose.yaml

## Project structure (partial) 🧭
- apps/
  - laravel-front/ — Laravel application used as the web UI
  - symfony-back/ — Symfony API and domain logic
  - python-llm/ — Python-based LLM components
- docs/ — Source of truth for documentation in Markdown
- services/ — Service definitions and local runtime helpers
- ui/ — UI assets (if any)
- compose.yaml — Docker Compose definitions

## Development 🛠️
- Voir docs/setup.md pour l’installation locale, les migrations et les workflows courants.
- Voir docs/services/* pour les notes spécifiques à chaque service.

## Contributing 🤝
- Utilisez Conventional Commits pour les messages (ex. : feat:, fix:, docs:).
- Ouvrez une PR avec une description concise et un lien vers les issues associées.

## License 📄
- Spécifiez la licence du projet ici.
