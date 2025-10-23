# Architecture consolidée 🏗️✨

Cette page reprend la vue d’ensemble consolidée de l’architecture de Huginn. Pour la version « source », voir aussi ../architecture.md 🔗.

## Panorama des composants 🧩
- 🌐 Frontend (Laravel) — Interface utilisateur consommant l’API backend.
- 🧱 Backend (Symfony) — Endpoints, logique métier, orchestration des services.
- 🧠 Service LLM (Python) — Génération/streaming, métriques Prometheus.
- 🐳 Docker Compose — Assemblage local des services.

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
3. Le Backend délègue au Service LLM (Python) si nécessaire (génération/streaming).
4. Les réponses remontent vers le Frontend. ✅

## Liens utiles 🔗
- Endpoint LLM par défaut : http://llm:8008/generate/stream
- Métriques : http://localhost:9108/metrics
