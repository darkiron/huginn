# Architecture consolidée 🏗️✨

Cette page présente une vue d’ensemble consolidée de l’architecture de Huginn, les flux de données et les points d’intégration clés. Elle est conçue pour être générique et durable, indépendamment des implémentations ponctuelles. 

## Panorama des composants 🧩
- 🌐 Frontend (Laravel) — Fournit l’interface utilisateur et consomme l’API backend.
- 🧱 Backend (Symfony) — Expose des endpoints, applique la logique métier et orchestre les services.
- 🧠 Service LLM (Python) — Encapsule la génération et le streaming, expose des métriques Prometheus.
- 🐳 Docker Compose — Relie et configure les services pour le dev local.

## Diagramme (Mermaid) 🗺️
```mermaid
flowchart LR
  subgraph UI[UI / Frontend (Laravel)]
    A[Client Web]
  end
  subgraph API[API / Backend (Symfony)]
    B[Contrôleurs
    + Cas d'usage]
  end
  subgraph LLM[Service LLM (Python)]
    C[HTTP generate/stream
    + CLI RNN]
    M[Metrics :9108 /metrics]
  end
  A -->|HTTP| B
  B -->|HTTP POST /generate/stream| C
  C -->|stream| B
  B -->|JSON| A
  M -.->|Prometheus scrape| Ext[(Observabilité)]
```

## Flux de données 🔄
1. L’utilisateur interagit avec le Frontend (Laravel).
2. Le Frontend appelle l’API du Backend (Symfony).
3. Le Backend applique la logique métier et délègue au Service LLM (Python) si nécessaire (génération/streaming).
4. Les réponses remontent vers le Frontend. ✅

## Points d’intégration clés 🔌
- URL LLM par défaut : `http://llm:8008/generate/stream` (configurable via `LLM_URL`).
- Métriques : `http://localhost:9108/metrics` exposé par le conteneur LLM.
- Volumes : `./ckpts -> /ckpts` (checkpoints), `./apps/python-llm -> /app/apps/python-llm`.

## Répertoires et fichiers utiles 📁
- apps/laravel-front — contrôleurs, routes, vues.
- apps/symfony-back — contrôleurs, domaine, cas d’usage.
  - src/Domain/Model/Prompt.php
  - src/Domain/Port/LLMGateway.php
  - src/Application/UseCase/GenerateStreamUseCase.php
  - src/Controller/LLMController.php
- apps/python-llm — composants LLM (llm_rnn, tokenizers, etc.).

