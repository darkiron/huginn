# Architecture 🏗️

## Overview
- 🌐 Frontend (Laravel) serves the user interface and talks to the Symfony backend.
- 🧱 Backend (Symfony) provides API endpoints, orchestrates domain logic, and delegates LLM‑related work to the Python service when needed.
- 🧠 LLM Service (Python) encapsulates model logic and streaming/generation features.
- 🐳 Docker Compose wires services together for local development.

## High‑level data flow 🔄
1. The user interacts with the Laravel frontend.
2. The frontend calls Symfony backend APIs.
3. The backend applies domain rules and, if needed, requests completions/streams from the Python LLM service.
4. Responses propagate back to the frontend. ✅

## Repositories and code of interest 📁
- apps/laravel-front — Laravel controllers, routes, views.
- apps/symfony-back — Symfony controllers, domain models, use cases.
  - src/Domain/Model/Prompt.php
  - src/Domain/Port/LLMGateway.php
  - src/Application/UseCase/GenerateStreamUseCase.php
  - src/Controller/LLMController.php
- apps/python-llm — Python LLM components (llm_rnn and more).

