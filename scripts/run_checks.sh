#!/usr/bin/env bash
set -euo pipefail

MODE="quick"
WITH_E2E=0
WITH_FRONTEND=0
KEEP_STACK=0

usage() {
  cat <<'EOF'
Usage: scripts/run_checks.sh [quick|full] [--with-e2e] [--with-frontend] [--keep-stack]

Modes:
  quick  Run checks that do not require local services or Docker Compose.
         Stages: Python import smoke, unit tests, integration tests.

  full   Start/validate Docker Compose and then run quick checks plus backend API smoke.
         Stages: Python import smoke, unit tests, integration tests, Docker stack health, API smoke.

Options:
  --with-e2e       Also run tests/e2e after integration tests.
  --with-frontend  In full mode, validate Streamlit frontend health too.
  --keep-stack     In full mode, leave Docker Compose running after checks finish.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    quick|full)
      MODE="$1"
      ;;
    --with-e2e)
      WITH_E2E=1
      ;;
    --with-frontend)
      WITH_FRONTEND=1
      ;;
    --keep-stack)
      KEEP_STACK=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

run_stage() {
  local name="$1"
  shift
  echo
  echo "=== ${name} ==="
  echo "+ $*"
  set +e
  "$@"
  local status=$?
  set -e
  if [[ "${status}" -ne 0 ]]; then
    echo "FAILED: ${name} (exit ${status})" >&2
    return "${status}"
  fi
  echo "PASSED: ${name}"
}

cleanup_stack() {
  if [[ "${MODE}" == "full" && "${KEEP_STACK}" -eq 0 ]]; then
    echo
    echo "=== Docker Compose cleanup ==="
    scripts/docker-down.sh || echo "WARNING: Docker Compose cleanup failed" >&2
  fi
}
trap cleanup_stack EXIT

cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-.}"

IMPORT_MODULES=(
  src.backend.main
  src.frontend.app
  src.backend.services.inventory.catalog
  src.backend.services.recommendations.ranker
  src.backend.services.finance.estimator
)
IMPORT_CODE='import importlib, sys
modules = sys.argv[1:]
failed = []
for module in modules:
    try:
        importlib.import_module(module)
        print(f"OK import {module}")
    except Exception as exc:
        failed.append((module, exc))
        print(f"FAIL import {module}: {exc}", file=sys.stderr)
if failed:
    raise SystemExit(1)
'

run_stage "Python import smoke (no services)" python -c "${IMPORT_CODE}" "${IMPORT_MODULES[@]}"
run_stage "Unit tests (no services)" python -m pytest tests/unit
run_stage "Integration tests (no Docker Compose required)" python -m pytest tests/integration

if [[ "${WITH_E2E}" -eq 1 ]]; then
  run_stage "E2E tests (optional)" python -m pytest tests/e2e
else
  echo
  echo "=== E2E tests (optional) ==="
  echo "SKIPPED: pass --with-e2e to run tests/e2e."
fi

if [[ "${MODE}" == "full" ]]; then
  run_stage "Docker Compose up (full mode)" scripts/docker-up.sh

  VALIDATE_ARGS=()
  if [[ "${WITH_FRONTEND}" -eq 1 ]]; then
    VALIDATE_ARGS+=(--include-frontend)
  fi
  run_stage "Docker stack health check (full mode)" python scripts/validate_stack.py "${VALIDATE_ARGS[@]}"
  run_stage "Backend API smoke (full mode)" python scripts/test_api.py
else
  echo
  echo "=== Docker stack health check (optional) ==="
  echo "SKIPPED: quick mode does not require Docker Compose; run 'scripts/run_checks.sh full' for full checks."
fi

printf '\nAll requested checks passed.\n'
