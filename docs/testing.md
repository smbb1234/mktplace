# Testing

This project uses `pytest` and groups tests by intent under `tests/unit`, `tests/integration`, and `tests/e2e`.

## Test categories

### Unit tests

Unit tests validate small functions, components, and services in isolation. They should be fast and should not require Docker.

Examples in this repo include:

- inventory loading and image path resolution,
- recommendation scoring/ranking logic,
- finance estimator formatting and calculations,
- Streamlit component rendering with fake Streamlit objects,
- repository/model tests that use in-memory SQLite.

Run unit tests locally with:

```bash
python -m pytest tests/unit
```

### Integration tests

Integration tests validate API routes and cross-module behaviour, usually through FastAPI `TestClient`. Many current integration tests are designed to run without Docker by using local test doubles, in-memory SQLite, or graceful handling of an unavailable database.

Run integration tests locally with:

```bash
python -m pytest tests/integration
```

For the most realistic integration environment, run the same command inside the combined app container after Docker Compose starts Postgres and service environment variables:

```bash
docker compose exec app python -m pytest tests/integration
```

### End-to-end tests

E2E tests exercise user-level flows across multiple API behaviours. In this MVP they are still backend/TestClient-oriented rather than browser-driven, but they cover broader flows such as chat, recommendations, catalog lookup, enquiry creation, and admin enquiry handling.

Run them locally with:

```bash
python -m pytest tests/e2e
```

Run them in the Docker stack for the closest match to the expected local runtime:

```bash
docker compose exec app python -m pytest tests/e2e
```

## Which tests need Docker?

Strictly required Docker dependencies are limited in the current suite because the tests are written to be lightweight for local development.

Use Docker for:

- validating the application against the real Compose service names and environment,
- verifying Postgres-backed enquiry/admin flows against the running `postgres` service,
- checking container startup, healthchecks, and port mappings,
- full-stack smoke checks that use host URLs (`localhost:8000`, `localhost:8501`).

Docker is not normally required for:

- pure unit tests,
- Streamlit component tests with fake Streamlit modules,
- ranking/filtering/finance helper tests,
- TestClient API tests that monkeypatch database/catalog dependencies or tolerate database-unavailable responses.

## Local quick test workflow

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m pytest tests/unit
python -m pytest tests/integration
python -m pytest tests/e2e
```

If you only need the fastest confidence check while editing UI or recommendation logic, start with:

```bash
python -m pytest tests/unit
```

## Full Docker validation workflow

1. Create `.env.docker` with container-friendly values. The important setting is that `DATABASE_URL` points at the Compose service name `postgres`, not `localhost`:

   ```bash
   cat > .env.docker <<'ENV'
   OPENAI_API_KEY=
   DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/mktplace
   POSTGRES_DB=mktplace
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   # The app binds FastAPI to 0.0.0.0 internally; this host is used by the colocated Streamlit client.
   FASTAPI_HOST=127.0.0.1
   FASTAPI_PORT=8000
   STREAMLIT_HOST=0.0.0.0
   STREAMLIT_PORT=8501
   INVENTORY_CSV_PATH=data/dataset.csv
   PLACEHOLDER_IMAGE_PATH=assets/placeholder.svg
   CHROMA_ENABLED=false
   CHROMA_DB_PATH=/app/vector_db
   ADMIN_TOKEN=
   ENV
   ```

2. Build and start services:

   ```bash
   docker compose up -d --build
   ```

3. Confirm services are running:

   ```bash
   docker compose ps
   ```

4. Run tests inside the combined app container:

   ```bash
   docker compose exec app python -m pytest tests/unit tests/integration tests/e2e
   ```

5. Validate backend endpoints from the host:

   ```bash
   curl -f http://localhost:8000/health
   curl -f http://localhost:8000/catalog/
   curl -f -X POST http://localhost:8000/chat/message \
     -H 'Content-Type: application/json' \
     -d '{"message":"I am looking to buy with a budget of £450 per month"}'
   ```

6. Validate frontend reachability:

   ```bash
   curl -f http://localhost:8501
   ```

7. Stop services:

   ```bash
   docker compose down
   ```

## Postgres unavailable and the offline enquiry queue

The enquiry API has a local fallback for database write failures:

1. A user submits an enquiry through `POST /enquiries/`.
2. If `LeadsRepository.create_enquiry()` raises a SQLAlchemy database error, the API writes the submitted payload to `data/offline_enquiries.jsonl`.
3. The API returns HTTP `202` with a message that the enquiry was received and queued.
4. Each line in `data/offline_enquiries.jsonl` is one JSON enquiry payload.

Recommended handling:

- Treat HTTP `202` as accepted-but-not-yet-persisted.
- Do not delete `data/offline_enquiries.jsonl` manually unless you intentionally want to discard queued enquiries.
- Restore Postgres first, then flush the queue.
- From Docker, flush with:

  ```bash
  docker compose exec app python -m src.backend.scripts.flush_offline_enquiries
  ```

- Or use the admin API route:

  ```bash
  curl -f -X POST http://localhost:8000/admin/flush_offline
  ```

  If `ADMIN_TOKEN` is set, include it as `X-Admin-Token`:

  ```bash
  curl -f -X POST http://localhost:8000/admin/flush_offline \
    -H "X-Admin-Token: $ADMIN_TOKEN"
  ```

The flush script retries queued rows one by one. Successfully persisted rows are removed. Failed rows are kept in the queue file for a later retry.
