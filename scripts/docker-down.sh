#!/usr/bin/env bash
set -euo pipefail

echo "Stopping Docker Compose stack..."
docker compose down
echo "Docker Compose stopped. Use 'docker compose ps' to confirm." 
