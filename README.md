# Huginn ✨

Bienvenue ! Huginn est une application IA multi‑services, pensée pour une expérience développeur fluide et des frontières claires entre les composants. 🙌

Ce que contient le dépôt :
- 🧱 Backend Symfony (apps/symfony-back)
- 🌐 Frontend Laravel (apps/laravel-front)
- 🧠 Service LLM Python (apps/python-llm)

Ce dépôt est un monorepo et inclut une configuration Docker Compose pour le développement local.

## Liens rapides 🔗
- 📚 Index de la documentation : docs/README.md
- 🗂️ Wiki (dans le dépôt) : docs/wiki/Home.md
- 🏗️ Architecture consolidée : docs/architecture.md
- 🧭 Documentation générale : docs/wiki/Documentation-Generique.md
- 🔗 GitHub Wiki (publié) : https://github.com/darkiron/huginn/wiki

## Démarrage (Docker) 🐳
1. Prérequis : Docker Desktop 4.x ou plus récent.
2. Depuis la racine du dépôt :
   - Copiez ou créez les fichiers d’environnement comme décrit dans docs/env.md.
   - Démarrez la stack : `docker compose up -d`
3. Ouvrez les services (valeurs par défaut) :
   - 🖥️ Frontend : http://localhost:8080 (à ajuster selon votre compose)
   - 🔙 API Backend : http://localhost:8000
   - 🧪 LLM Python (selon compose.yaml)

## Structure du projet (partielle) 🧭
- apps/
  - laravel-front/ — Application Laravel pour l’interface Web
  - symfony-back/ — API Symfony et logique métier
  - python-llm/ — Composants LLM en Python
- docs/ — Référentiel principal de la documentation (Markdown)
- services/ — Définition des services et helpers d’exécution locale
- ui/ — Actifs UI (si présents)
- compose.yaml — Définition Docker Compose

## Développement 🛠️
- Voir docs/setup.md pour l’installation locale, les migrations et les workflows courants.
- Voir docs/services/* pour les notes spécifiques à chaque service.

## Contribuer 🤝
- Utilisez Conventional Commits pour les messages (ex. : feat:, fix:, docs:).
- Ouvrez une PR avec une description concise et un lien vers les issues associées.

## Licence 📄
- Spécifiez la licence du projet ici.
