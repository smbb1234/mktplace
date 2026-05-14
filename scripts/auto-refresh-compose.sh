#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

COMPOSE_CMD=(${COMPOSE_CMD:-docker compose})
POLL_INTERVAL="${POLL_INTERVAL:-2}"
DEBOUNCE_SECONDS="${DEBOUNCE_SECONDS:-1}"
WATCH_PATHS=(${WATCH_PATHS:-src app docker scripts requirements.txt docker-compose.yml docker-compose-ubuntu.yml .env.example README.md docs})

usage() {
  cat <<'USAGE'
Usage: scripts/auto-refresh-compose.sh

Watches project code/configuration paths and restarts Docker Compose when they change.

Environment variables:
  COMPOSE_CMD        Compose command to run (default: docker compose)
  POLL_INTERVAL      Seconds between filesystem scans (default: 2)
  DEBOUNCE_SECONDS   Seconds to wait after a detected change before restart (default: 1)
  WATCH_PATHS        Space-separated paths to watch (default: src app docker scripts requirements.txt docker-compose.yml docker-compose-ubuntu.yml .env.example README.md docs)
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

snapshot() {
  local existing=()
  local path
  for path in "${WATCH_PATHS[@]}"; do
    [[ -e "${path}" ]] && existing+=("${path}")
  done

  if ((${#existing[@]} == 0)); then
    return 0
  fi

  find "${existing[@]}" \
    \( -path '*/.git' -o -path '*/.venv' -o -path '*/__pycache__' -o -path '*/.pytest_cache' -o -path '*/node_modules' \) -prune \
    -o -type f -printf '%p %T@ %s\n' \
    | sort
}

restart_stack() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Change detected. Restarting Docker Compose stack..."
  "${COMPOSE_CMD[@]}" down
  "${COMPOSE_CMD[@]}" up -d --build
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Docker Compose stack restarted."
}

echo "Watching for code changes under: ${WATCH_PATHS[*]}"
echo "Using compose command: ${COMPOSE_CMD[*]}"
echo "Press Ctrl+C to stop."

previous="$(snapshot)"

while true; do
  sleep "${POLL_INTERVAL}"
  current="$(snapshot)"
  if [[ "${current}" != "${previous}" ]]; then
    sleep "${DEBOUNCE_SECONDS}"
    current="$(snapshot)"
    restart_stack
    previous="$(snapshot)"
  fi
done
