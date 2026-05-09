# Quickstart: AI Car Buying Assistant MVP Technical Plan

## Goal

Run the planned local MVP architecture with a Streamlit frontend, FastAPI backend, PostgreSQL database, CSV inventory source, and optional ChromaDB semantic matching.

## Prerequisites

- Python 3.12.3
- PostgreSQL 15+ running locally
- OpenAI API key for assistant responses
- Existing project files in `data/` and `assets/`

## Planned Environment Variables

```bash
OPENAI_API_KEY=
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/mktplace
INVENTORY_CSV_PATH=data/dataset.csv
PLACEHOLDER_IMAGE_PATH=assets/placeholder.svg
CHROMA_ENABLED=false
CHROMA_PERSIST_DIR=.chroma
STREAMLIT_SERVER_PORT=8501
FASTAPI_PORT=8000
```

## Planned Startup Sequence

1. Start PostgreSQL locally.
2. Install Python dependencies from `requirements.txt` plus any plan-approved additions for FastAPI, SQLAlchemy, psycopg, and ChromaDB.
3. Start the FastAPI backend.
4. On backend startup, validate and normalize `data/dataset.csv`, load placeholder image config from `data/schema.json`, and warm the in-memory inventory cache.
5. If `CHROMA_ENABLED=true`, build or load persisted vehicle embeddings.
6. Start Streamlit and connect it to the local backend base URL.
7. Open the customer page and verify the assistant can reach first recommendation state after collecting intent and monthly budget.
8. Open the admin dashboard and verify leads/status flow against PostgreSQL-backed demo records.

## Planned Manual Smoke Checks

### Customer journey

1. Start a new session and provide intent plus monthly budget.
2. Verify 1–3 cars appear with placeholder image, match score, finance estimate, and explanation.
3. Change fuel or transmission preference and verify refreshed results within the same session.
4. Compare two vehicles and confirm required side-by-side fields render.
5. Open finance estimate and confirm disclaimer is visible.
6. Submit enquiry and verify confirmation message.

### Admin journey

1. Open dashboard.
2. Confirm the new enquiry appears with status `New`.
3. Open lead detail and verify AI summary, selected car, and viewed/compared vehicles are present.
4. Update lead status and add a note.
5. Refresh and confirm persistence.

## Planned Implementation Boundaries

- No production deployment steps.
- No authentication workflow.
- No external finance or dealer integrations.
- No real payment or credit decisioning.