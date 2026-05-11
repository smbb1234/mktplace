# Implementation Plan: AI Car Buying Assistant MVP — Docker Connectivity Validation

**Branch**: `feature/20260508-ai-car-buying-assistant-mvp` | **Date**: 2026-05-10 | **Spec**: specs/ai-car-buying-assistant-mvp/spec.md (primary)
**Input**: This plan adapts the MVP to ensure all Docker Compose services install cleanly and the application verifies connectivity end-to-end (Postgres, Chroma, backend, frontend, Portainer).

**Note**: Generated via `/speckit.plan`. Focus: automated service validation and DB CRUD smoke test to reduce connectivity issues.

## Summary

Add a Docker-first workflow with automated validation: after `docker compose up -d --build`, a host-run script verifies each service is reachable. Postgres connectivity is proven by creating, reading, and dropping a temporary table; backend `/health` is checked; Streamlit responds on 8501; Chroma server heartbeat is reachable; Portainer UI is reachable. Quickstart documents a one-command validation flow.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, Streamlit, SQLAlchemy, psycopg[binary], Pydantic v2, Requests, Tenacity, ChromaDB (optional)  
**Storage**: PostgreSQL 16 (docker `postgres`), optional Chroma server (docker `chroma`)  
**Testing**: pytest for unit/integration + host-side validation script (`scripts/validate_stack.py`)  
**Target Platform**: Linux/macOS dev machines via Docker Compose  
**Project Type**: Web service (FastAPI) + UI (Streamlit) + local data services  
**Performance Goals**: Not performance-focused; goal is reliable local startup + connectivity checks  
**Constraints**: Local-only per constitution; no production auth/integration; avoid unnecessary complexity  
**Scale/Scope**: MVP developer environment validation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Local-only runtime: satisfied via Docker Compose with mounted data/assets.
- No production integrations: satisfied; Postgres and Chroma are local-only.
- Safe finance wording: unaffected by connectivity tasks.
- Keep complexity minimal: use a single validation script and optional Compose healthchecks.

Gate status: PASS.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── backend/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── scripts/
├── frontend/
│   └── api_client/
└── shared/

tests/
├── unit/
└── integration/

docker/
└── Dockerfile

scripts/
├── docker-up.sh
├── docker-down.sh
├── init_db_container.sh
└── validate_stack.py (NEW)

docker-compose.yml
```

**Structure Decision**: Single repository with `src/backend` + `src/frontend`, Docker-first runtime, and one multi-target `docker/Dockerfile` for both Python app services. A new host-run `scripts/validate_stack.py` performs connectivity checks post `docker compose up`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Phase 1 Test Plan (Data & Persistence)

Goal: Thoroughly validate local data ingestion and persistence before backend features build on top.

- CSV Loader: valid rows parse; malformed JSON in `Car Inventory Data`/`Pricing Details` handled; missing optional fields defaulted; unknown columns ignored; type coercion where safe.
- Image Resolver: absolute/relative paths; missing files fall back to placeholder; `is_placeholder_image` correctness.
- Inventory Catalog: filtering by budget, fuel, transmission; boundary conditions; deterministic ordering; unique ID listing; cache warm/reload behaviour.
- Database Models: enums and field constraints align with schemas; basic create/round-trip using local engine.
- Repositories: session and enquiry CRUD semantics using an in-memory SQLite engine to avoid external dependency in unit tests; enum/status constraints enforced.
- Integration Smoke: bootstrap script creates tables; repositories operate against Docker Postgres (`T014`).

Test Tasks Reference: see `T014a`–`T014d` in tasks.md plus `T014` for integration coverage.
