# Implementation Plan: AI Car Buying Assistant MVP

**Branch**: `feature/20260508-ai-car-buying-assistant-mvp` | **Date**: 2026-05-09 | **Spec**: `/specs/ai-car-buying-assistant-mvp/spec.md`
**Input**: Feature specification from `/specs/ai-car-buying-assistant-mvp/spec.md`

**Note**: This plan covers technical design only. It intentionally excludes implementation tasks and code changes.

## Summary

Build a local-only AI car buying demo that combines a Streamlit customer/admin UI, a FastAPI backend, PostgreSQL persistence for leads and session artifacts, CSV-backed inventory ingestion, and an OpenAI-driven advisor workflow. The system must keep the assistant active throughout browsing, generate explainable recommendations from local inventory only, support comparison and finance estimates, and produce a structured admin summary without implying real finance approval or live dealer integration.

## Technical Context

**Language/Version**: Python 3.12.3  
**Primary Dependencies**: FastAPI, Streamlit, Pydantic v2, SQLAlchemy, psycopg, OpenAI Python SDK, optional OpenAI Agents SDK, ChromaDB, pandas  
**Storage**: PostgreSQL for operational data, local CSV file for inventory source of truth, local filesystem for placeholder/static images, ChromaDB for optional semantic retrieval  
**Testing**: pytest, httpx for API tests, Playwright or Streamlit app smoke tests, contract validation for OpenAPI examples  
**Target Platform**: Local Linux/macOS/Windows development machine, single-user demo environment  
**Project Type**: Local web application with separate backend API and Streamlit frontend  
**Performance Goals**: First recommendation within 3 conversational turns; refreshed recommendations within 1 second after preference changes on inventory sizes up to 200 rows; dashboard/API responses under 500ms p95 excluding LLM latency  
**Constraints**: Fully local runtime except OpenAI API calls; demo/sample data only; no real finance approval, credit checks, payment processing, or live integrations; assistant must use local CSV inventory and local image references/placeholder only  
**Scale/Scope**: Single demo deployment, up to a few concurrent local sessions, inventory under 1,000 vehicles, one customer journey flow and one simple admin dashboard

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Pass: The architecture preserves the required journey `Search -> AI Recommendation -> Compare -> Finance Estimate -> Enquiry -> Admin Follow-up`.
- Pass: The assistant remains the primary interaction model, with Streamlit UI organized around a persistent side chat and visual recommendation workspace.
- Pass: Recommendations remain explainable and inventory-bound to local CSV records and local placeholder/image assets.
- Pass: Finance handling is explicitly demo-only with mandatory disclaimer handling in UI and API responses.
- Pass: Proposed persistence and integrations stay within MVP constraints: local PostgreSQL, local CSV, local images, optional local ChromaDB, no production auth or external dealer/finance systems.
- Post-design re-check: Pass. Phase 1 artifacts keep the advisor-led journey intact and do not introduce production-only complexity.

## Technical Architecture

### System Overview

```text
Streamlit UI
├── Customer journey page
│   ├── persistent assistant panel
│   ├── recommendations workspace
│   ├── comparison panel
│   ├── finance estimate drawer
│   └── enquiry form
└── Admin dashboard
    ├── lead list
    ├── lead detail with AI summary
    └── lead status/notes editor

FastAPI backend
├── session/orchestration API
├── inventory and recommendation API
├── comparison API
├── finance estimate API
├── enquiry API
└── admin dashboard API

Data services
├── CSV inventory loader/cache
├── image resolver
├── recommendation engine
├── finance estimator
├── conversation state service
├── enquiry/lead repository
└── optional vector retrieval service

Persistence
├── PostgreSQL
│   ├── enquiries
│   ├── customer sessions/preferences
│   ├── shortlist/comparisons
│   ├── lead status/notes
│   └── AI summaries/audit metadata
└── ChromaDB
    └── embedded vehicle descriptions and summaries
```

### Component Decisions

- Streamlit is the frontend shell because it is sufficient for a local MVP, supports fast admin/customer views, and keeps UI complexity low.
- FastAPI owns all domain logic and state mutation so Streamlit stays thin and can be replaced later without rewriting business logic.
- PostgreSQL is used instead of file-only persistence because the MVP explicitly needs lead lifecycle updates, notes, shortlist state, and admin refresh-safe persistence.
- CSV remains the inventory source of truth; a backend loader normalizes JSON-in-cell data into typed models and serves cached records to all recommendation and comparison flows.
- ChromaDB is optional and should augment ranking only for semantic similarity between customer intent and vehicle descriptions; deterministic filters and score rules remain primary.
- OpenAI Agents SDK is optional. Default architecture should use a single orchestrator service built on the OpenAI Responses/Chat API with explicit tools. Agents SDK is acceptable only if it does not obscure deterministic inventory/tool constraints.

### Request and Interaction Flow

1. Streamlit starts or restores a customer session.
2. Customer sends a chat message.
3. FastAPI conversation endpoint stores the message, updates extracted preferences, and determines whether minimum inputs for recommendations are satisfied.
4. Recommendation service filters inventory deterministically by hard constraints, optionally augments ranking with ChromaDB similarity, computes or reuses match scores, and returns up to 3 results.
5. LLM generates explanation text strictly from supplied structured recommendation context.
6. Streamlit renders cards in the main workspace while keeping the assistant thread visible.
7. Comparison, finance estimate, shortlist, and enquiry actions call dedicated backend endpoints but reuse the same session context.
8. Enquiry submission persists operational records and triggers generation of an admin-facing customer summary.
9. Admin dashboard reads PostgreSQL-backed enquiry, summary, shortlist, and status records.

## Project Structure

### Documentation (this feature)

```text
specs/20260508-ai-car-buying-assistant-mvp/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── api.yaml
```

### Source Code (repository root)

```text
src/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   └── deps/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── ai/
│   │   ├── inventory/
│   │   ├── finance/
│   │   └── leads/
│   ├── repositories/
│   └── main.py
├── frontend/
│   ├── app.py
│   ├── pages/
│   ├── components/
│   ├── state/
│   └── api_client/
└── shared/
    ├── config/
    ├── types/
    └── utils/

data/
├── dataset.csv
├── datasetSample.csv
└── schema.json

assets/
├── placeholder.svg
└── vehicles/

tests/
├── unit/
├── integration/
├── contract/
└── e2e/
```

**Structure Decision**: Use a single repository with clear backend/frontend separation under `src/` so the MVP can keep Streamlit and FastAPI decoupled while sharing schemas, config, and utility code. This minimizes future migration cost while staying lightweight for a local demo.

## API Design

### Core Endpoints

- `POST /api/v1/sessions`: create or resume a customer session.
- `GET /api/v1/sessions/{session_id}`: fetch session state, shortlist, selected comparison set, and latest recommendations.
- `POST /api/v1/chat/messages`: submit a customer/admin-visible message and receive assistant response plus optional UI actions.
- `POST /api/v1/recommendations/query`: compute recommendations from current or explicit preferences.
- `POST /api/v1/recommendations/refine`: apply preference deltas and return refreshed recommendations with change explanation.
- `POST /api/v1/comparisons`: create/update comparison set for 2–3 vehicles.
- `POST /api/v1/finance-estimates`: compute an indicative finance estimate for a vehicle and input deposit/term override.
- `POST /api/v1/shortlist/items`: add shortlist item.
- `DELETE /api/v1/shortlist/items/{vehicle_id}`: remove shortlist item.
- `POST /api/v1/enquiries`: submit a lead/enquiry.
- `GET /api/v1/admin/leads`: list leads and summary metrics.
- `GET /api/v1/admin/leads/{lead_id}`: fetch a lead with AI summary, recommended cars, compared cars, and notes.
- `PATCH /api/v1/admin/leads/{lead_id}`: update lead status and admin notes.

### API Behaviour Rules

- Recommendation endpoints must return only vehicles derived from `data/dataset.csv` normalization.
- Finance endpoints must include the canonical disclaimer in every response payload.
- Chat endpoint responses should include structured UI directives such as `show_recommendations`, `refresh_comparison`, `show_no_results_guidance`, and `prompt_for_missing_fields`.
- Admin endpoints remain unauthenticated for MVP but should be isolated under `/admin` routes and configurable for future auth.

## CSV and Image Handling Approach

### Inventory Ingestion

- `data/dataset.csv` is the authoritative inventory input for MVP.
- The loader parses per-row JSON from `Car Inventory Data` and `Pricing Details`, ignoring non-MVP columns unless needed for explanation fallbacks.
- Parsed records are validated into typed `InventoryVehicle` and `VehiclePricing` models.
- Loader runs on backend startup and can expose a manual refresh command for demo data changes.
- Parsed inventory is cached in memory for low-latency recommendation refreshes.

### Image Resolution

- Preferred image source is a path from normalized CSV data if added later.
- Current default behavior is to use `assets/placeholder.svg` for all vehicles, as required by the spec and schema.
- Image resolver returns a stable local path or URL consumable by Streamlit, plus a flag indicating placeholder fallback.
- Recommendation and comparison payloads should carry `image_path`, `is_placeholder_image`, and optional `image_alt_text`.

### Data Quality Handling

- Missing non-critical attributes render as `N/A` in UI and are excluded from score components that depend on them.
- Missing critical identifiers or pricing fields should mark a record unavailable for recommendation until corrected.
- The backend should emit startup warnings for malformed JSON rows rather than silently accepting them.

## AI Agent Flow

### Orchestration Strategy

- Use a backend conversation orchestrator with deterministic tools for preference extraction, inventory query, comparison assembly, finance estimation, and summary generation.
- LLM output must never directly invent cars, prices, finance values, or inventory attributes; all such data must come from backend tools.
- A structured system prompt should encode the advisor tone, finance safety wording, and mandatory ask-before-filter behavior.

### Conversation Stages

1. Greeting and discovery: capture intent, monthly budget, deposit, family/lifestyle, fuel/transmission, and key concerns.
2. Minimum viable recommendation trigger: after intent and monthly budget are captured, return 1–3 recommendations.
3. Guided refinement: allow natural-language preference changes and explain why recommendations changed.
4. Deepening intent: offer comparison, finance estimate, shortlist, or enquiry based on user readiness.
5. Lead capture and summary: generate structured admin summary after enquiry or strong intent signals.

### Tooling Decision

- Default recommendation: implement explicit tool-calling with the OpenAI Python SDK first.
- Use OpenAI Agents SDK only if it materially simplifies orchestration without reducing determinism, observability, or tool constraints.
- Keep a service abstraction so either orchestration mode can be swapped behind the same interface.

## Database Tables

- `customer_sessions`: session metadata, status, timestamps, current stage.
- `session_messages`: chat transcript with role, content, tool metadata, and turn order.
- `session_preferences`: normalized extracted preferences and latest confidence.
- `session_shortlist_items`: shortlisted vehicle IDs and timestamps.
- `session_comparisons`: grouped comparison selections and derived context.
- `finance_estimates`: persisted indicative estimates shown to customers.
- `enquiries`: submitted lead/contact records with selected vehicle and buying context.
- `lead_status_history`: lead state changes with actor and timestamp.
- `lead_notes`: admin notes and follow-up entries.
- `ai_customer_summaries`: structured summary JSON and rendered text.

Detailed fields and relationships are defined in `data-model.md`.

## Local Setup Approach

- Run PostgreSQL locally via Docker Compose or local service install.
- Store configuration in `.env` with values for database URL, OpenAI API key, CSV path, placeholder image path, and optional ChromaDB path.
- Start backend FastAPI app and frontend Streamlit app as separate local processes.
- On startup, backend validates CSV/schema alignment, loads inventory into cache, and initializes or reconnects to ChromaDB if enabled.
- ChromaDB embedding build should be an explicit startup/init task so demo users can skip it for deterministic-only matching.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM invents unsupported cars or finance claims | Breaks trust and violates MVP boundaries | Force all recommendation facts through deterministic tool outputs and structured response schemas |
| CSV quality issues or malformed JSON cells | Recommendation failures or bad cards | Validate on load, log row-level errors, skip invalid rows, provide sample CSV contract |
| Streamlit state drift from backend session state | Inconsistent shortlist/comparison experience | Treat backend as source of truth and refresh Streamlit state from API responses after every mutation |
| ChromaDB adds noise or slows local startup | Confusing rankings or setup friction | Make semantic ranking optional and secondary to rule-based filtering; allow startup without embeddings |
| Finance wording appears too definitive | Compliance/safety issue | Centralize disclaimer constants and include them in all finance API and UI components |
| Local image files are absent | Broken UI cards | Use required placeholder image fallback and surface missing-path diagnostics |
| Admin dashboard grows into production auth/reporting scope | Scope creep | Keep admin views limited to lead tracking, summaries, notes, and status changes only |

## Complexity Tracking

No constitution violations identified. No exceptional complexity justification is required for this planning phase.
