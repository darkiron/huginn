# Backend — Symfony 🔙

Notes spécifiques au backend Symfony. Pour des détails d'implémentation, voir le code sous apps/symfony-back.

## LLMGateway — Client Python LLM
- Implémentation: `apps/symfony-back/src/Infrastructure/LLM/PythonLLMClient.php`
- Rôle: émettre une requête HTTP POST vers l'endpoint du service LLM et consommer une réponse en streaming.
- URL par défaut: `llm_url` (paramètre Symfony) ou variable d'env `LLM_URL`; fallback: `http://llm:8008/generate/stream`.

Extrait important:
- Streaming via `HttpClientInterface` avec `buffer: false` puis itération avec `$this->httpClient->stream($response)`.
- Les chunks sont relayés tels quels au consommateur (contrôleur/cas d'usage) pour un flux temps réel.

## Configuration
- Voir `compose.yaml` -> service `symfony-back`:
  - `LLM_URL` et `LLM_METRICS_URL` injectés via env.
- Paramétrage côté Symfony (parameters, services) pour `llm_url`.

## Cas d'usage & contrôleurs
- Domaine: `src/Domain/Model/Prompt.php`, `src/Domain/Port/LLMGateway.php`
- Application: `src/Application/UseCase/GenerateStreamUseCase.php`
- Interface: `src/Controller/LLMController.php`

## Dépannage
- 502/timeout en streaming: vérifier l'URL LLM, que le conteneur `llm` tourne, et aucun proxy n'interrompt la connexion.
- CORS/front: s'assurer que le contrôleur renvoie les en-têtes nécessaires selon le front.

Voir aussi:
- [LLM-Service-Python](LLM-Service-Python) — endpoint attendu et métriques 🧠
- [Architecture](Architecture) — flux entre services 🗺️