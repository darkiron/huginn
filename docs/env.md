# Environment and configuration

Do not commit secrets. Prefer local-only files and examples.

Global
- compose.yaml may define service ports and volumes.
- You can override or add an .env file at the repo root for Compose if needed.

Symfony backend (apps/symfony-back)
- .env: base configuration committed for defaults.
- .env.local: local overrides (ignored by Git).
- .env.dev: development overrides (ignored by Git per .gitignore).
- Important keys:
  - APP_SECRET — Symfony app secret.
  - DATABASE_URL — if using a database.

Laravel frontend (apps/laravel-front)
- .env — local settings; an example may be available via .env.example.
- Important keys:
  - APP_KEY — use php artisan key:generate to set.
  - APP_URL — base URL for the app.
  - Backend API endpoint configuration (if applicable via env variables).

Python LLM (apps/python-llm)
- Typically uses a .env or config file; document variables relevant to the service (e.g., model paths, ports, API keys).

Recommendations
- Provide .env.example files where possible.
- Never commit credentials. Use .gitignore to keep local secrets out of version control.
