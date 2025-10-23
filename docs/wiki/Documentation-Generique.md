# Documentation générale 🧭📚

Cette page rassemble des informations génériques et transverses utiles à tous les contributeurs et utilisateurs. Elle met l’accent sur la clarté, la typographie, et les points d’entrée communs. ✨

## Principes de base ✅
- Simplicité d’abord : expliquer le nécessaire, lier le reste.
- Cohérence : mêmes noms, mêmes chemins, mêmes options.
- Emojis avec parcimonie 😄 : pour signaler les sections et les alertes.

## Typographie (FR) ✍️
- Espaces insécables fines avant : « : », « ; », « ! », « ? ». Exemple : « Docker : démarrer… ».
- Guillemets français « … » pour les citations, apostrophe typographique ’ si possible.
- Tirez le meilleur des tirets : tiret court « - » pour les listes, tiret moyen « – » pour les incises.

Astuce : dans Markdown, collez une espace fine insécable (U+202F) avant « : ; ! ? » lorsque vous éditez depuis un éditeur compatible.

## Endpoints et services 🔌
- Backend (Symfony) : sert l’API HTTP.
- Service LLM (Python) :
  - Génération HTTP attendue par le backend : `http://llm:8008/generate/stream`
  - Métriques Prometheus : `http://localhost:9108/metrics`

Voir aussi :
- [Architecture](Architecture) — Vue consolidée et diagramme Mermaid 🗺️
- [LLM RNN CLI](LLM-RNN-CLI) — Génération via Docker Compose 🐳

## Développement local 🛠️
- Démarrage rapide : `docker compose up -d`
- Frontend : http://localhost:8080 (ou 8081 selon compose)
- Backend : http://localhost:8000
- LLM (metrics) : http://localhost:9108/metrics

Consultez aussi :
- [Setup](Setup) — Installation et commandes utiles
- [Environment](Environment) — Variables d’environnement et secrets

## Conventions de commit 🧾
- Utiliser Conventional Commits : `feat:`, `fix:`, `docs:`, etc.
- Ajouter un gitemoji au besoin : `docs: 📝 …`, `ci: 🤖 …`, `feat: ✨ …`.

## Qualité et liens 🔗
- Utiliser des liens relatifs entre pages wiki.
- Préférer des titres courts et descriptifs.
- Éviter les redondances : lier les pages d’autorité (source of truth).

Bonnes contributions ! 🤝