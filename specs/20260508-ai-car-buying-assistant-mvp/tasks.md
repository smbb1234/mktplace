# Tasks: AI Car Buying Assistant MVP

## Phase 0: Foundation Setup

- [x] T001 [P] Create the project skeleton for backend, frontend, shared code, tests, and assets directories.
  - Target files: `src/backend/`, `src/frontend/`, `src/shared/`, `tests/`, `assets/vehicles/`
  - Dependencies: none
  - Notes: Keep the folder split aligned with `plan.md`.

- [x] T002 [P] Add local environment configuration examples and runtime defaults.
  - Target files: `.env.example`, `src/shared/config/settings.py`, `src/backend/core/config.py`, `src/frontend/api_client/config.py`
  - Dependencies: T001
  - Notes: Include OpenAI key, PostgreSQL URL, CSV path, placeholder image path, Streamlit port, FastAPI port, and optional Chroma settings.

- [x] T003 [P] Update Python dependency manifest for the planned stack.
  - Target files: `requirements.txt`
  - Dependencies: T001
  - Notes: Add FastAPI, Streamlit, SQLAlchemy, psycopg, pandas, Pydantic v2, OpenAI SDK, ChromaDB, pytest, httpx, and any lightweight helpers needed for local parsing.

- [x] T004 [P] Define shared constants for inventory, finance disclaimer, and recommendation thresholds.
  - Target files: `src/shared/config/constants.py`
  - Dependencies: T002
  - Notes: Include canonical finance disclaimer text, match score cutoff, minimum recommendation inputs, and debounce timing from `data/schema.json`.

- [x] T005 Validate the project scaffold and configuration paths exist and are importable.
  - Target files: `src/backend/`, `src/frontend/`, `src/shared/`, `.env.example`
  - Dependencies: T001, T002, T003, T004
  - Notes: Smoke-check directory layout and settings import resolution.

## Docker Compose: Dev runtime (required)

These tasks make Docker Compose the default local runtime and ensure source mounts allow live editing in VS Code.

- [x] T070 Create `.env.docker.example` and make Compose use `.env.docker` for container runtimes.
  - Target files: `.env.docker.example`, `docker-compose.yml`
  - Dependencies: T002
  - Notes: `.env.docker` contains container hostnames (postgres, chroma, backend) and in-container paths such as `/app/data` and `/app/assets`.

- [x] T071 Ensure Compose service volume mounts expose source code, `./data` and `./assets` into containers.
  - Target files: `docker-compose.yml`, `docker/Dockerfile.backend`, `docker/Dockerfile.frontend`
  - Dependencies: T001, T070
  - Notes: Volumes should enable live code edits from VS Code with `uvicorn --reload` and Streamlit auto-reload.

- [x] T072 Add developer helper scripts for Docker Compose: `scripts/docker-up.sh`, `scripts/docker-down.sh`.
  - Target files: `scripts/docker-up.sh`, `scripts/docker-down.sh`
  - Dependencies: T070, T071
  - Notes: Scripts should copy `.env.docker.example` to `.env.docker` if missing, then run `docker compose up -d --build` or `docker compose down` respectively.

- [x] T073 Add a small helper to run DB initialization in the backend container: `scripts/init_db_container.sh`.
  - Target files: `scripts/init_db_container.sh`
  - Dependencies: T072, T011, T013
  - Notes: Script runs `docker compose exec backend python -m src.backend.scripts.init_db` and reports success/failure.

- [x] T074 Update README and Quickstart to document Docker-first workflow and live-edit behaviour.
  - Target files: `README.md`, `specs/20260508-ai-car-buying-assistant-mvp/quickstart.md`
  - Dependencies: T070, T071, T072, T076

- [x] T075 Add container healthchecks for key services (optional but recommended).
  - Target files: `docker-compose.yml`
  - Dependencies: T070, T071
  - Notes: Define `healthcheck` for `postgres` (pg_isready), `backend` (curl /health), and `chroma` (HTTP heartbeat) to improve `depends_on` readiness.

- [x] T076 Add automated validation script for service connectivity.
  - Target files: `scripts/validate_stack.py`
  - Dependencies: T070, T071, T072
  - Notes: Script should (1) connect to Postgres on `localhost:5433` and run create/read/delete table, (2) check backend `/health`, (3) check Streamlit root, (4) check Chroma heartbeat, (5) check Portainer UI.

- [ ] T077 Validate Docker stack end-to-end (automated + minimal manual spot checks).
  - Target files: none
  - Dependencies: T073, T075, T076
  - Notes: Run `docker compose up -d --build`, then `python scripts/validate_stack.py`; confirm backend health and Streamlit UI render.

## Phase 1: Local Data and Persistence Foundation

### User Story 1 - Local inventory and images

- [x] T006 [P] Implement CSV inventory loader for JSON-in-cell records.
  - Target files: `src/backend/services/inventory/csv_loader.py`, `src/backend/models/inventory.py`
  - Dependencies: T002, T004
  - Notes: Parse `data/dataset.csv` columns `Car Inventory Data` and `Pricing Details` into typed models.

- [x] T007 [P] Implement vehicle image resolution with placeholder fallback.
  - Target files: `src/backend/services/inventory/image_resolver.py`, `assets/placeholder.svg`
  - Dependencies: T002, T004, T006
  - Notes: Use placeholder image for MVP unless a local image path exists; expose `is_placeholder_image`.

- [x] T008 Add inventory normalization and caching service.
  - Target files: `src/backend/services/inventory/catalog.py`, `src/backend/services/inventory/__init__.py`
  - Dependencies: T006, T007
  - Notes: Provide in-memory inventory lookup, vehicle-by-id access, and filtered query helpers.

- [x] T009 Add local demo inventory validation against the schema contract.
  - Target files: `tests/unit/test_inventory_loader.py`, `tests/unit/test_image_resolver.py`
  - Dependencies: T006, T007, T008
  - Notes: Verify JSON parsing, missing-field handling, and placeholder fallback.

### User Story 2 - PostgreSQL persistence

- [x] T010 [P] Define PostgreSQL database models and enums.
  - Target files: `src/backend/models/session.py`, `src/backend/models/leads.py`, `src/backend/models/finance.py`, `src/backend/models/common.py`
  - Dependencies: T002, T004
  - Notes: Model sessions, preferences, shortlist, comparisons, enquiries, status history, notes, and AI summaries.

- [x] T011 [P] Implement database session and engine configuration.
  - Target files: `src/backend/core/database.py`, `src/backend/core/__init__.py`
  - Dependencies: T002, T010
  - Notes: Configure SQLAlchemy/psycopg for local PostgreSQL and provide session lifecycle helpers.

- [x] T012 Implement repository layer for sessions, enquiries, and admin lead updates.
  - Target files: `src/backend/repositories/session_repo.py`, `src/backend/repositories/enquiry_repo.py`, `src/backend/repositories/lead_repo.py`
  - Dependencies: T010, T011
  - Notes: Keep persistence isolated from API route code.

- [x] T013 Add database migration/bootstrap script for local tables.
  - Target files: `src/backend/scripts/init_db.py`, `src/backend/scripts/__init__.py`
  - Dependencies: T010, T011
  - Notes: Create tables for MVP and seed any required defaults.

- [ ] T014 Add persistence smoke tests for session and enquiry records.
  - Target files: `tests/integration/test_database_bootstrap.py`, `tests/integration/test_repositories.py`
  - Dependencies: T012, T013
 - [x] T014 Add persistence smoke tests for session and enquiry records.
   - Target files: `tests/integration/test_database_bootstrap.py`, `tests/integration/test_repositories.py`
   - Dependencies: T012, T013

#### Phase 1 — Unit Tests (expanded coverage)

- [ ] T014a Unit: CSV loader edge cases and schema alignment.
 - [x] T014a Unit: CSV loader edge cases and schema alignment.
  - Target files: `tests/unit/test_csv_loader_edges.py`
  - Dependencies: T006, T009
  - Notes: Cover invalid/malformed JSON in `Car Inventory Data`/`Pricing Details`, missing optional fields with sensible defaults, unknown columns ignored, inconsistent types coerced or flagged.

- [ ] T014b Unit: Image resolver path handling.
 - [x] T014b Unit: Image resolver path handling.
  - Target files: `tests/unit/test_image_resolver_paths.py`
  - Dependencies: T007
  - Notes: Validate absolute vs relative image paths, nonexistent files fallback to placeholder, `is_placeholder_image` correctness.

- [ ] T014c Unit: Inventory catalog filtering and caching.
 - [x] T014c Unit: Inventory catalog filtering and caching.
  - Target files: `tests/unit/test_catalog_filters.py`
  - Dependencies: T008
  - Notes: Budget boundary conditions (exact cutoffs), fuel/transmission filters, deterministic ordering, uniqueness of IDs, cache warm/reload behaviour.

- [ ] T014d Unit: Repository method interfaces with lightweight in-memory DB.
 - [x] T014d Unit: Repository method interfaces with lightweight in-memory DB.
  - Target files: `tests/unit/test_repositories_unit.py`
  - Dependencies: T012
  - Notes: Use SQLite in-memory engine to validate repository CRUD semantics for sessions and enquiries without requiring Docker Postgres; assert enum/status constraints and basic validation at repository boundary.

### User Story 3 - Local vector database setup

- [ ] T015 [P] Add ChromaDB configuration and local persistence path handling.
 - [x] T015 [P] Add ChromaDB configuration and local persistence path handling.
  - Target files: `src/backend/services/vectorstore/chroma_config.py`, `src/backend/services/vectorstore/__init__.py`
  - Dependencies: T002
  - Notes: Keep Chroma optional and disabled by default if the plan allows.

- [ ] T016 Implement vehicle embedding and semantic lookup helpers.
 - [x] T016 Implement vehicle embedding and semantic lookup helpers.
  - Target files: `src/backend/services/vectorstore/vehicle_index.py`
  - Dependencies: T015, T008
  - Notes: Index vehicle descriptions only; semantic retrieval must remain secondary to deterministic filtering.

- [ ] T017 Add vector store validation smoke test.
 - [x] T017 Add vector store validation smoke test.
  - Target files: `tests/integration/test_vectorstore.py`
  - Dependencies: T015, T016

## Phase 2: Backend API and Core Services

### User Story 4 - FastAPI backend and app bootstrap

- [x] T018 [P] Create FastAPI application entrypoint and router registration.
  - Target files: `src/backend/main.py`, `src/backend/api/__init__.py`, `src/backend/api/routes/__init__.py`
  - Dependencies: T011, T012

- [x] T019 [P] Add API health and readiness endpoints.
  - Target files: `src/backend/api/routes/health.py`
  - Dependencies: T018

- [x] T020 Add backend startup wiring for inventory load, vector index, and database initialization.
  - Target files: `src/backend/core/startup.py`, `src/backend/main.py`
  - Dependencies: T008, T013, T015, T018

- [ ] T021 Add backend smoke test for startup and health endpoints.
 - [x] T021 Add backend smoke test for startup and health endpoints.
  - Target files: `tests/integration/test_backend_health.py`
  - Dependencies: T019, T020

### User Story 5 - AI assistant conversation flow and preference extraction

- [ ] T022 [P] Define chat/session API schemas.
 - [x] T022 [P] Define chat/session API schemas.
  - Target files: `src/backend/schemas/chat.py`, `src/backend/schemas/session.py`
  - Dependencies: T010, T018

- [ ] T023 [P] Implement preference extraction from chat messages.
 - [x] T023 [P] Implement preference extraction from chat messages.
  - Target files: `src/backend/services/ai/preference_extractor.py`, `src/backend/services/ai/__init__.py`
  - Dependencies: T004, T022
  - Notes: Extract intent, budget, deposit, fuel, transmission, family size, running cost, and timeframe.

- [ ] T024 Implement conversation state orchestration service.
 - [x] T024 Implement conversation state orchestration service.
  - Target files: `src/backend/services/ai/conversation_orchestrator.py`
  - Dependencies: T008, T012, T022, T023
  - Notes: Keep the assistant active while recommendations, comparison, finance, and enquiry are displayed.

- [ ] T025 Add chat message persistence and session update flow.
 - [x] T025 Add chat message persistence and session update flow.
  - Target files: `src/backend/api/routes/chat.py`, `src/backend/services/ai/chat_service.py`
  - Dependencies: T018, T024, T012

- [ ] T026 Add conversation flow tests for greeting, extraction, and turn updates.
 - [ ] T026 Add conversation flow tests for greeting, extraction, and turn updates.
  - Target files: `tests/integration/test_chat_flow.py`, `tests/unit/test_preference_extractor.py`
  - Dependencies: T023, T024, T025

### User Story 6 - Intent-based recommendation logic and match scoring

- [ ] T027 [P] Implement match score calculation service.
 - [x] T027 [P] Implement match score calculation service.
  - Target files: `src/backend/services/recommendations/match_score.py`
  - Dependencies: T004, T008
  - Notes: Use provided total match score when available, otherwise compute weighted score from budget, intent, and lifestyle/family.

- [ ] T028 Implement deterministic recommendation filtering and ranking.
 - [x] T028 Implement deterministic recommendation filtering and ranking.
  - Target files: `src/backend/services/recommendations/ranker.py`, `src/backend/services/recommendations/filtering.py`
  - Dependencies: T008, T016, T027, T024
  - Notes: Enforce budget, transmission, fuel, and availability constraints before optional vector similarity.

- [ ] T029 Implement recommendation explanation generation input builder.
 - [x] T029 Implement recommendation explanation generation input builder.
  - Target files: `src/backend/services/recommendations/explanations.py`
  - Dependencies: T028
  - Notes: Produce structured explanation context for the LLM without inventing vehicle facts.

- [ ] T030 Add recommendation API endpoints for query and refinement.
 - [x] T030 Add recommendation API endpoints for query and refinement.
  - Target files: `src/backend/api/routes/recommendations.py`, `src/backend/schemas/recommendations.py`
  - Dependencies: T018, T022, T027, T028, T029

- [ ] T031 Add recommendation logic tests for scoring, filtering, and no-results guidance.
 - [ ] T031 Add recommendation logic tests for scoring, filtering, and no-results guidance.
  - Target files: `tests/unit/test_match_score.py`, `tests/unit/test_recommendation_ranker.py`, `tests/integration/test_recommendation_api.py`
  - Dependencies: T027, T028, T030

### User Story 7 - Finance estimate and disclaimer

- [ ] T032 [P] Implement finance estimate calculation service.
 - [x] T032 [P] Implement finance estimate calculation service.
  - Target files: `src/backend/services/finance/estimator.py`, `src/backend/services/finance/__init__.py`
  - Dependencies: T004, T008
  - Notes: Use per-car pricing defaults and clamp demo inputs safely.

- [ ] T033 Add finance estimate API endpoint and response schema.
 - [x] T033 Add finance estimate API endpoint and response schema.
  - Target files: `src/backend/api/routes/finance.py`, `src/backend/schemas/finance.py`
  - Dependencies: T018, T032

- [ ] T034 Add finance disclaimer constants and response enforcement.
 - [ ] T034 Add finance disclaimer constants and response enforcement.
  - Target files: `src/shared/config/constants.py`, `src/backend/services/finance/estimator.py`, `src/frontend/components/finance_disclaimer.py`
  - Dependencies: T004, T032, T033

- [ ] T035 Add finance calculation tests and disclaimer validation.
 - [ ] T035 Add finance calculation tests and disclaimer validation.
  - Target files: `tests/unit/test_finance_estimator.py`, `tests/integration/test_finance_api.py`
  - Dependencies: T032, T033, T034

### User Story 8 - Comparison, shortlist, and enquiry APIs

- [ ] T036 Implement shortlist persistence service.
 - [x] T036 Implement shortlist persistence service.
  - Target files: `src/backend/services/leads/shortlist_service.py`
  - Dependencies: T012, T024

- [ ] T037 Add shortlist API endpoints.
 - [x] T037 Add shortlist API endpoints.
  - Target files: `src/backend/api/routes/shortlist.py`
  - Dependencies: T018, T036

- [ ] T038 Implement comparison assembly service for 2–3 vehicles.
 - [x] T038 Implement comparison assembly service for 2–3 vehicles.
  - Target files: `src/backend/services/recommendations/comparison_service.py`
  - Dependencies: T008, T028, T032

- [ ] T039 Add comparison API endpoint and schema.
 - [x] T039 Add comparison API endpoint and schema.
  - Target files: `src/backend/api/routes/comparisons.py`, `src/backend/schemas/comparisons.py`
  - Dependencies: T018, T038

- [ ] T040 Implement enquiry capture service and AI summary generation.
 - [x] T040 Implement enquiry capture service and AI summary generation.
  - Target files: `src/backend/services/leads/enquiry_service.py`, `src/backend/services/ai/customer_summary.py`
  - Dependencies: T012, T024, T032

- [ ] T041 Add enquiry API endpoint and schema.
 - [x] T041 Add enquiry API endpoint and schema.
  - Target files: `src/backend/api/routes/enquiries.py`, `src/backend/schemas/enquiries.py`
  - Dependencies: T018, T040

- [ ] T042 Add comparison, shortlist, and enquiry tests.
 - [ ] T042 Add comparison, shortlist, and enquiry tests.
  - Target files: `tests/integration/test_comparison_api.py`, `tests/integration/test_shortlist_api.py`, `tests/integration/test_enquiry_api.py`
  - Dependencies: T037, T039, T041

### User Story 9 - Admin dashboard and lead management

- [ ] T043 Implement admin lead listing and detail services.
 - [x] T043 Implement admin lead listing and detail services.
  - Target files: `src/backend/services/leads/admin_dashboard.py`
  - Dependencies: T012, T040

- [ ] T044 Add admin API endpoints for lead list, detail, status update, and notes.
 - [x] T044 Add admin API endpoints for lead list, detail, status update, and notes.
  - Target files: `src/backend/api/routes/admin.py`
  - Dependencies: T018, T043

- [ ] T045 Add admin status history and notes persistence behavior.
 - [ ] T045 Add admin status history and notes persistence behavior.
  - Target files: `src/backend/services/leads/status_service.py`, `src/backend/services/leads/notes_service.py`
  - Dependencies: T012, T043, T044

- [ ] T046 Add admin dashboard API tests for status updates and notes.
 - [ ] T046 Add admin dashboard API tests for status updates and notes.
  - Target files: `tests/integration/test_admin_api.py`
  - Dependencies: T044, T045

## Phase 3: Streamlit Customer UI

### User Story 10 - Customer-facing assistant workspace

- [x] T047 [P] Create Streamlit app entrypoint and page routing.
  - Target files: `src/frontend/app.py`, `src/frontend/pages/__init__.py`
  - Dependencies: T002, T018

- [x] T048 [P] Implement API client wrapper for frontend/backend communication.
  - Target files: `src/frontend/api_client/client.py`, `src/frontend/api_client/__init__.py`
  - Dependencies: T002, T018, T030, T033, T037, T039, T041, T044

- [x] T049 Implement persistent assistant sidebar/chat component.
  - Target files: `src/frontend/components/chat_panel.py`, `src/frontend/state/session_state.py`
  - Dependencies: T047, T048

- [x] T050 Implement recommendation card rendering with image and score.
  - Target files: `src/frontend/components/recommendation_cards.py`
  - Dependencies: T007, T028, T048

- [x] T051 Implement finance estimate display with disclaimer.
  - Target files: `src/frontend/components/finance_panel.py`, `src/frontend/components/finance_disclaimer.py`
  - Dependencies: T034, T048

- [ ] T052 Add customer UI validation and empty-state handling.
  - Target files: `src/frontend/components/validation.py`, `src/frontend/components/empty_states.py`
  - Dependencies: T049, T050, T051

- [ ] T053 Add customer journey smoke test plan for Streamlit UI.
  - Target files: `tests/e2e/test_customer_journey.py`
  - Dependencies: T047, T049, T050, T051, T052

### User Story 11 - Live preference refinement and result refresh

- [ ] T054 Implement preference refinement controls and refresh trigger.
  - Target files: `src/frontend/components/preference_controls.py`
  - Dependencies: T048, T049, T050

- [ ] T055 Implement no-results guidance and relaxation suggestions in the UI.
  - Target files: `src/frontend/components/no_results.py`
  - Dependencies: T030, T054

- [ ] T056 Add refinement refresh tests for chat-driven changes.
  - Target files: `tests/e2e/test_refinement_refresh.py`
  - Dependencies: T054, T055

### User Story 12 - Car detail, comparison, shortlist, and enquiry UI

- [ ] T057 Implement car detail section for selected recommendation.
  - Target files: `src/frontend/components/car_detail.py`
  - Dependencies: T050, T048

- [ ] T058 Implement 2–3 car comparison section.
  - Target files: `src/frontend/components/comparison_view.py`
  - Dependencies: T039, T048

- [ ] T059 Implement shortlist controls and shortlist summary panel.
  - Target files: `src/frontend/components/shortlist_panel.py`
  - Dependencies: T037, T050, T057

- [ ] T060 Implement enquiry form and submission confirmation.
  - Target files: `src/frontend/components/enquiry_form.py`
  - Dependencies: T041, T051, T059

- [ ] T061 Add UI validation and submission error handling for comparison, shortlist, and enquiry flows.
  - Target files: `src/frontend/components/validation.py`, `src/frontend/components/errors.py`
  - Dependencies: T057, T058, T059, T060

## Phase 4: Local Demo Data and End-to-End Validation

### User Story 13 - Local demo data and content

- [ ] T062 Review and normalize local demo inventory rows for MVP usage.
  - Target files: `data/dataset.csv`, `data/datasetSample.csv`
  - Dependencies: T006, T008
  - Notes: Keep demo records aligned to the required recommendation, comparison, and enquiry scenarios.

- [ ] T063 Confirm schema settings for placeholder image and recommendation thresholds.
  - Target files: `data/schema.json`
  - Dependencies: T004, T007

- [ ] T064 Seed any local demo notes or sample leads needed for dashboard walkthroughs.
  - Target files: `src/backend/scripts/seed_demo_data.py`
  - Dependencies: T013, T040, T043

### User Story 14 - Basic validation and error handling

- [ ] T065 Add shared validation helpers for required enquiry fields, budget ranges, and comparison counts.
  - Target files: `src/shared/utils/validation.py`
  - Dependencies: T004, T022, T041, T039

- [ ] T066 Add backend-level validation/error handlers for API responses.
  - Target files: `src/backend/api/errors.py`, `src/backend/core/error_handlers.py`
  - Dependencies: T018, T065

- [ ] T067 Add frontend-level error display and retry guidance.
  - Target files: `src/frontend/components/errors.py`, `src/frontend/components/validation.py`
  - Dependencies: T066

### User Story 15 - Final MVP smoke test

- [ ] T068 Build a complete end-to-end local smoke test covering customer and admin flows.
  - Target files: `tests/e2e/test_mvp_smoke.py`
  - Dependencies: T053, T056, T061, T064, T067
  - Notes: Cover greeting, discovery, recommendation, refinement, comparison, finance, shortlist, enquiry, summary, and admin status update.

- [ ] T069 Document the final local demo runbook and smoke-test checklist.
  - Target files: `specs/20260508-ai-car-buying-assistant-mvp/quickstart.md`, `README.md`
  - Dependencies: T068

## Execution Order Notes

- Tasks marked `[P]` can be started in parallel once their dependencies are satisfied.
- The recommended implementation order is T001 through T005, then the data/persistence foundation, then the backend APIs, then the Streamlit UI, and finally the demo data and smoke test tasks.
- Do not add production auth, live integrations, real credit checks, payment processing, or deployment tasks.