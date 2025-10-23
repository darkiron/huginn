# Troubleshooting 🛟

See repository details : ../../docs/troubleshooting.md 🔗

## Common items ✅
- 🐳 Docker ports conflict — adjust compose.yaml or stop conflicting services.
- ⚠️ Symfony 500 — set APP_SECRET, clear cache, check var/log.
- 🔑 Laravel APP_KEY — run `php artisan key:generate`.
- 🔌 LLM not reachable — verify port mapping and URLs.
