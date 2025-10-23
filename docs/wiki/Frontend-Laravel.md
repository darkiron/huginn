# Frontend — Laravel 🌐

Notes spécifiques au frontend Laravel (apps/laravel-front).

## Démarrage en dev
- Servi par le conteneur `laravel-front` (voir compose.yaml):
  - Commande: artisan serve sur 0.0.0.0:8080 (via script de démarrage).
  - Port exposé par compose: 8081 -> 8080
- Code monté en volume: `./apps/laravel-front:/var/www/html`

## Communication avec le backend
- Cible par défaut du backend selon compose: http://symfony-back:8080 (interne réseau Docker) — l'exposition hôte est http://localhost:8082
- Configurer l'URL API côté front selon vos conventions (env/config).

## Débogage rapide
- Erreurs 404/500: vérifier les routes Laravel et la correspondance avec les endpoints du backend.
- CORS: ajuster les en-têtes côté backend si nécessaire.

Voir aussi:
- [Backend-Symfony](Backend-Symfony) — endpoints et streaming 🔙
- [Architecture](Architecture) — flux entre UI/API/LLM 🗺️