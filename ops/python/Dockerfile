# ops/python/Dockerfile
FROM python:3.11-slim AS deps
WORKDIR /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Crée le venv
RUN python -m venv /opt/venv

# Libs runtime pour Torch CPU
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas0 \
 && rm -rf /var/lib/apt/lists/*

# Installe dans le venv (⚠️ chaque bloc de commandes commence par RUN)
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install "numpy<2"
RUN /opt/venv/bin/pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu
RUN /opt/venv/bin/pip install psutil prometheus_client

# ---- Runtime
FROM python:3.11-slim AS app
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas0 \
 && rm -rf /var/lib/apt/lists/*

# Amène le venv prêt
COPY --from=deps /opt/venv /opt/venv

# User non-root
RUN useradd -ms /bin/bash runner && chown -R runner:runner /app /opt/venv
USER runner

# Le code est monté en volume par docker compose
CMD ["/opt/venv/bin/python", "-m", "http.server", "8000"]
