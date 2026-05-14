#!/usr/bin/env bash
set -euo pipefail

echo "Initializing database inside app container (SQLAlchemy create_all)..."

# Prefer docker compose v2; fallback to v1 if needed
if command -v docker &>/dev/null && docker compose version &>/dev/null; then
	DOCKER_COMPOSE=(docker compose)
elif command -v docker-compose &>/dev/null; then
	DOCKER_COMPOSE=(docker-compose)
else
	echo "docker compose not found" >&2
	exit 1
fi

"${DOCKER_COMPOSE[@]}" exec app python -m src.backend.scripts.init_db

echo "init_db completed"
