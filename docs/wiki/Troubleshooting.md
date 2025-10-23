# Troubleshooting 🛟

Problèmes courants et correctifs. Voir aussi ../troubleshooting.md pour plus de cas.

## LLM — erreurs fréquentes
- ModuleNotFoundError: No module named 'llm_rnn'
  - Exécuter dans le conteneur `llm` (docker compose exec llm …) où PYTHONPATH est défini.
  - En local, définir `PYTHONPATH=apps/python-llm`.
- FileNotFoundError: /ckpts/rnn.pt
  - Vérifier l'existence de `./ckpts/rnn.pt` (hôte) et le volume `./ckpts:/ckpts`.
  - Ajuster `--ckpt` si nécessaire.
- Flux interrompu côté backend
  - Vérifier `LLM_URL` et l'accessibilité de `http://llm:8008/generate/stream` depuis le conteneur `symfony-back`.
  - Désactiver proxies intermédiaires qui bufferisent le stream.

## Backend (Symfony)
- Timeout sur requêtes stream
  - S'assurer que `timeout`=0 côté HttpClient et que l'upstream répond bien par fragments.
- CORS
  - Configurer les en-têtes selon le domaine du frontend.

## Frontend (Laravel)
- 404 sur endpoints API
  - Vérifier le prefix/base URL et l'exposition du backend (8082).

## Métriques et observabilité
- LLM metrics: http://localhost:9108/metrics (ou http://llm:9108/metrics entre conteneurs)
  - Si vide: attendre 1–2s; sinon vérifier `METRICS_PORT` et le supervisor.

Voir aussi:
- [LLM RNN CLI](LLM-RNN-CLI)
- [Backend-Symfony](Backend-Symfony)