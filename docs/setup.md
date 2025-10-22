# Setup ⚙️

## Prerequisites ✅
- 🐳 Docker Desktop (recommended for the quickest start)
- 🧰 Git
- 💻 Optional for native runs: PHP 8.2+, Composer, Node 18+, Python 3.10+

## Quickstart with Docker Compose 🚀
1. Clone the repository and cd into it.
2. Create environment files as needed (see docs/env.md).
3. Start services: `docker compose up -d`
4. Check logs if needed: `docker compose logs -f --tail=200`
5. Open the services in your browser as described in README.md.

> Astuce : si un service ne se lance pas, vérifiez les logs et les ports utilisés (voir Troubleshooting). 🔍

## Native development (optional) 🖥️
- Symfony backend (apps/symfony-back)
  - Copy .env to .env.local and configure DB/APP_SECRET as needed.
  - `composer install`
  - `php bin/console doctrine:database:create` (if using Doctrine/SQL)
  - `symfony server:start` or `php -S localhost:8000 -t public`
- Laravel frontend (apps/laravel-front)
  - `cp .env.example .env` then `php artisan key:generate` (if example exists)
  - `composer install && php artisan migrate`
  - `php artisan serve`
- Python LLM (apps/python-llm)
  - Create a virtualenv, install dependencies, start the service as documented in that app.

## Data and persistence 💾
- The default compose.yaml may mount volumes under data/ and services/; review it before first start.

