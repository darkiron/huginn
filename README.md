# Huginn

Huginn is a multi-service AI application composed of:
- Symfony backend (apps/symfony-back)
- Laravel frontend (apps/laravel-front)
- Python LLM service (apps/python-llm)

This repository is structured as a monorepo and includes a Docker Compose setup for local development.

Quick links
- Documentation index: docs/README.md
- GitHub Wiki source (to copy into your repo wiki): docs/wiki/Home.md

Getting started (Docker)
1. Prerequisites: Docker Desktop 4.x or newer.
2. From the repository root:
   - Copy or create necessary env files as described in docs/env.md.
   - Start the stack: docker compose up -d
3. Open the services (default assumptions):
   - Frontend: http://localhost:8080 (adjust if your compose uses a different port)
   - Backend API: http://localhost:8000
   - Python LLM: http://localhost:9000 or as defined in compose.yaml

Project structure (partial)
- apps/
  - laravel-front/ — Laravel application used as the web UI
  - symfony-back/ — Symfony API and domain logic
  - python-llm/ — Python-based LLM components
- docs/ — Source of truth for documentation in Markdown
- services/ — Service definitions and local runtime helpers
- ui/ — UI assets (if any)
- compose.yaml — Docker Compose definitions

Development
- See docs/setup.md for detailed local setup, database migrations, and common workflows.
- See docs/services/* for service-specific notes.

Contributing
- Use Conventional Commits for messages (e.g., feat:, fix:, docs:).
- Open a PR with a concise description and a link to related issues.

License
- Specify your project license here.
