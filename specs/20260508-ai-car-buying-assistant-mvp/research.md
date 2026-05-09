# Research: AI Car Buying Assistant MVP

## Decision 1: Use Streamlit plus FastAPI rather than a Streamlit-only app

- Decision: Separate the UI and application logic into a Streamlit frontend and FastAPI backend.
- Rationale: The customer journey and admin flow both need conversational state, recommendation logic, finance calculations, and persistence. Keeping these concerns in FastAPI preserves a clean domain boundary, makes contract definition straightforward, and reduces the risk of embedding too much logic in Streamlit callbacks.
- Alternatives considered: Streamlit-only architecture. Rejected because it would couple UI state too tightly to business logic and make future API testing, contract testing, and replacement of the frontend materially harder.

## Decision 2: Keep CSV as source of truth and normalize at startup

- Decision: Treat `data/dataset.csv` as the authoritative demo inventory source and parse the JSON-in-cell columns into validated in-memory models on backend startup.
- Rationale: The spec explicitly requires using the local CSV inventory and pricing details. Startup normalization gives low-latency recommendation refreshes and a single consistent representation for comparison, finance, and explanation generation.
- Alternatives considered: Query CSV directly on each request. Rejected because repeated parsing would add latency, duplicate validation logic, and complicate recommendation consistency.

## Decision 3: Use PostgreSQL for operational persistence

- Decision: Store enquiries, session preferences, shortlist state, lead status, notes, and AI summaries in PostgreSQL.
- Rationale: Although file-based storage could satisfy minimal persistence, the required admin dashboard, status transitions, and refresh-safe lead updates are materially easier and more reliable in PostgreSQL.
- Alternatives considered: JSON or SQLite file persistence. Rejected because the user explicitly requested PostgreSQL and because lead workflow data benefits from stronger relational modeling.

## Decision 4: Use deterministic recommendation filtering with optional semantic augmentation

- Decision: Base recommendation eligibility on deterministic filters and scoring rules first, with ChromaDB used only as an optional semantic ranking assist.
- Rationale: The constitution requires explainable, inventory-grounded recommendations. Deterministic filtering guarantees compliance with hard constraints like budget, transmission, and fuel preference, while semantic search can improve explanation and fallback ranking when intent is qualitative.
- Alternatives considered: LLM-only recommendations or vector-only retrieval. Rejected because they reduce traceability and make it easier to drift from explicit customer constraints.

## Decision 5: Start with OpenAI SDK tool-calling, keep Agents SDK optional

- Decision: Implement the AI advisor as a tool-driven orchestrator using the standard OpenAI SDK first, with an abstraction layer that could support the OpenAI Agents SDK later.
- Rationale: The MVP needs tight control over allowed tools, response shape, finance disclaimers, and inventory grounding. Direct tool-calling is easier to reason about and debug for a local MVP.
- Alternatives considered: Adopt OpenAI Agents SDK immediately. Rejected for the initial plan because it may add abstraction without enough benefit at MVP scale.

## Decision 6: Use placeholder image fallback as the default image policy

- Decision: Serve a single placeholder image for all vehicles until explicit per-vehicle local image paths are added.
- Rationale: The current schema and specification require placeholder fallback behavior, and the existing inventory structure does not yet define a reliable image field contract.
- Alternatives considered: Require image paths before planning. Rejected because it would block the MVP and contradict the current assumptions.

## Decision 7: Keep admin access local and unauthenticated for MVP

- Decision: Do not add production-style authentication or authorization in the technical plan beyond route separation and future-ready boundaries.
- Rationale: The MVP is explicitly local-only and out of scope for production deployment. Adding full auth would increase complexity without improving core demo value.
- Alternatives considered: Full role-based auth. Rejected because it violates MVP scope discipline.