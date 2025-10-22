# Troubleshooting

Docker compose fails to start
- Run: docker compose ps and docker compose logs -f
- Check ports in compose.yaml for conflicts on your machine.

Symfony returns 500 errors
- Ensure APP_SECRET is set in .env.local.
- Clear cache: php bin/console cache:clear
- Check logs under apps/symfony-back/var/log/

Laravel shows APP_KEY error
- Run: php artisan key:generate
- Ensure .env exists and contains APP_KEY.

Python LLM service not reachable
- Verify container/service port mapping.
- Confirm the backend is using the correct LLM endpoint.
