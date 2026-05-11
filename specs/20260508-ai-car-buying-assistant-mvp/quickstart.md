# Quickstart — AI Car Buying Assistant MVP

1. Start Docker Compose (build and run):

```bash
docker compose up -d --build
```

2. Wait for services, then validate stack:

```bash
python scripts/validate_stack.py
```

3. Normalize demo data (optional):

```bash
python -m src.backend.scripts.normalize_demo_data
```

4. Seed demo enquiries into the DB:

```bash
DATABASE_URL=postgresql+psycopg://car_user:car_password@localhost:5433/car_mvp \
  /home/srujan/Documents/repo/mktplace/.venv/bin/python -m src.backend.scripts.seed_demo_data
```

5. Run unit and integration tests:

```bash
/home/srujan/Documents/repo/mktplace/.venv/bin/python -m pytest tests/unit -q
/home/srujan/Documents/repo/mktplace/.venv/bin/python -m pytest tests/integration -q
```

6. Run E2E smoke tests (optional):

```bash
/home/srujan/Documents/repo/mktplace/.venv/bin/python -m pytest tests/e2e -q
```

7. Flush any offline enquiries (if DB was down earlier):

```bash
curl -X POST -H "X-Admin-Token: <token>" http://localhost:8000/admin/flush_offline
```
# Quickstart: Docker-First Local Run + Connectivity Validation

## Goal

Run the MVP locally via Docker Compose (backend, frontend, Postgres, optional Chroma, Portainer) and validate connectivity automatically, including a Postgres CRUD smoke test.

## Prerequisites

- Docker Desktop / Docker Engine with Compose v2
- Python 3.11+ on host (to run the validation script)
- OpenAI API key (optional for local UI exploration)

## 1) Configure Docker env

Copy or edit the Docker runtime env file. The repo ships `.env.docker` already; if missing, run `scripts/docker-up.sh` once to generate it from an example.

Key defaults (container network):
- `POSTGRES_DB=car_mvp`
- `POSTGRES_USER=car_user`
- `POSTGRES_PASSWORD=car_password`
- `DATABASE_URL=postgresql+psycopg://car_user:car_password@postgres:5432/car_mvp`

Host ports:
- Backend: http://localhost:8000
- Frontend: http://localhost:8501
- Postgres: localhost:5433 → container 5432
- Chroma: http://localhost:8001 (optional)
- Portainer: https://localhost:9443

## 2) Start the stack

```bash
./scripts/docker-up.sh
docker compose ps
```

Optionally initialize DB tables (SQLAlchemy `create_all`) inside the backend container:

```bash
./scripts/init_db_container.sh
```

## 3) Validate connectivity (automated)

Run the host-side validation to confirm all services are reachable and Postgres supports basic CRUD:

```bash
python scripts/validate_stack.py
```

What it checks:
- Postgres: create → read → drop a temp table using `psycopg` on `localhost:5433`
- Backend: `GET /health` returns `{ "status": "ok" }`
- Frontend: `GET /` responds (200/302)
- Chroma: heartbeat endpoint responds (if service is up)
- Portainer: UI responds over HTTPS (status 200/302/401 acceptable)

## 4) Explore locally

- Frontend: open http://localhost:8501
- Backend: open http://localhost:8000/health

## 5) Stop the stack

```bash
./scripts/docker-down.sh
```

## Notes

- The validation script requires `requests` and `psycopg[binary]` (included in `requirements.txt`).
- Chroma is optional; failures are reported but won’t block the rest of the stack.
- Keep credentials demo-only per the constitution; do not add production complexity.