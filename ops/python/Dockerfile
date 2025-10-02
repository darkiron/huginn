FROM python:3.11-slim

WORKDIR /app

# deps build utiles
RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc g++ make libopenblas-dev \
  && rm -rf /var/lib/apt/lists/*

# copie d'abord le pyproject pour profiter du cache
COPY apps/python-llm/pyproject.toml /app/pyproject.toml
COPY apps/python-llm/llm_markov /app/llm_markov
COPY apps/python-llm/llm_rnn    /app/llm_rnn

# install torch CPU + ton paquet
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir .
