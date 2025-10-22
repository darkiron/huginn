# Python LLM Service

Location: apps/python-llm

Overview
- Provides LLM-related capabilities (e.g., generation/streaming). Current code includes llm_rnn/ components.

Local development
- Recommended: use Docker Compose.
- Native: create a virtual environment, install dependencies, run the service entrypoint (document or add a CLI as needed).

Configuration
- Common env vars include model paths, ports, and provider credentials. See docs/env.md.

Interfaces
- Consumed by the Symfony backend through an LLM gateway/adapter.
