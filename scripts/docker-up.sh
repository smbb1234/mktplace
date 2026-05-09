#!/usr/bin/env bash
set -euo pipefail

# Copy example env if missing
if [ ! -f .env.docker ]; then
  if [ -f .env.docker.example ]; then
    cp .env.docker.example .env.docker
    echo "Created .env.docker from .env.docker.example"
  else
    echo ".env.docker.example not found; please create .env.docker manually" >&2
  fi
fi

echo "Building and starting Docker Compose stack..."
docker compose up -d --build
echo "Docker Compose started. Use 'docker compose ps' to check services." 
