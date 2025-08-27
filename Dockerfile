# ===== STAGE 1: build dependencies =====
FROM python:3.13-slim-bookworm AS builder

# No pyc files, unbuffered stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libssl-dev \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# copy deps files for caching
COPY pyproject.toml uv.lock ./

# install deps and clean uv cache
RUN uv sync --locked && uv cache clean

# copy project files
COPY . /app

# ===== STAGE 2: final image =====
FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# copy only needed files from build stage
COPY --from=builder /app /app
COPY --from=builder /root/.local /root/.local

ENV PATH="/root/.local/bin/:$PATH"

EXPOSE 8000
CMD ["./docker-entrypoint.sh"]
