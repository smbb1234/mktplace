# Feature Specification: AI Car Buying Assistant MVP

**Feature Branch**: `feature/20260508-ai-car-buying-assistant-mvp`  
**Created**: 2026-05-08  
**Status**: Draft  
**Input**: User description: "Create a product specification for the AI Car Buying Assistant MVP."

## User Scenarios & Testing (mandatory)

### User Story 1 - Conversational Discovery to First Recommendation (Priority: P1)

A prospect lands on the MVP and is welcomed by the AI assistant. The assistant conducts a short discovery conversation, gathers intent, budget, fuel/transmission and lifestyle preferences, then presents 1–3 recommended cars from the local CSV inventory with images, match scores, finance estimates, and an explanation for each.

**Why this priority**: This delivers the core value: an advisor-led buying experience with immediate, explainable recommendations.

**Independent Test**: Start with a fresh session, provide discovery inputs, and verify at least one recommendation card appears with image, score, and finance estimate sourced from the CSV inventory.

**Acceptance Scenarios**:

1. Given a fresh session and loaded CSV inventory, When the user answers discovery questions (intent, budget, family size, fuel/transmission), Then the system shows 1–3 recommended cars with images, match scores, and indicative finance estimates.
2. Given the assistant has user inputs, When it generates recommendations, Then each recommendation includes an AI explanation mapping choices (intent/budget/lifestyle) to vehicle attributes.
3. Given images linked in CSV, When recommendations render, Then each card loads the local image file or a fallback placeholder if missing.
4. Given finance is demo-only, When estimates are shown, Then a disclaimer states estimates are indicative only and subject to approval.

---

### User Story 2 - Live Preference Refinement (Priority: P1)

While viewing recommendations, the user updates preferences via the assistant (e.g., switches to automatic transmission, adjusts monthly budget). The recommendation list refreshes instantly to reflect the new constraints and the AI explains the changes.

**Why this priority**: Ensures an iterative, agent-led journey where the advisor adapts to evolving needs.

**Independent Test**: Change one preference (e.g., fuel type) and verify the recommendation set and explanations update accordingly from the CSV inventory.

**Acceptance Scenarios**:

1. Given recommended cars are shown, When the user changes a preference in chat, Then results refresh and the assistant explains the updated fit.
2. Given updated constraints eliminate some cars, When no items meet the criteria, Then the assistant suggests relaxing constraints or alternative trade-offs.

---

### User Story 3 - Side-by-Side Comparison (Priority: P1)

The user selects 2–3 cars to compare. A comparison view shows key attributes and suitability notes side by side, including price, monthly estimate, mileage, fuel type, transmission, body type, suitability, running cost indication, and value-for-money explanation.

**Why this priority**: Enables confident decision-making by clarifying trade-offs.

**Independent Test**: Select 2 cars from recommendations and open the comparison view to verify required fields and AI explanations are present for both.

**Acceptance Scenarios**:

1. Given a shortlist of two cars, When opening comparison, Then both cars appear with all required comparison attributes populated from CSV.
2. Given different trims/specs, When compared, Then the AI adds context about suitability and value-for-money based on user intent and constraints.

---

### User Story 4 - Finance Estimate (Priority: P1)

For any recommended or compared car, the user can view a basic finance estimate showing vehicle price, deposit amount, finance term, example interest rate, and an estimated monthly payment, with clear indicative-only wording.

**Why this priority**: Budget fit is central to buying decisions; estimates must be visible and safe.

**Independent Test**: Open finance estimate for a recommended car and verify all fields calculate/display and the disclaimer renders.

**Acceptance Scenarios**:

1. Given a selected car, When viewing finance details, Then price, deposit, term, example rate, and estimated monthly appear with an “indicative only” disclaimer.
2. Given a user changes deposit or term, When recalculated, Then the monthly estimate updates accordingly without implying approval.

---

### User Story 5 - Enquiry Capture (Priority: P1)

The user submits an enquiry for a selected car. The form captures full name, email, phone, preferred contact method/time, selected car, monthly budget, deposit amount, and buying timeframe.

**Why this priority**: Converts interest into a lead for follow-up.

**Independent Test**: Submit an enquiry and verify it is stored locally and appears in the admin dashboard with captured details.

**Acceptance Scenarios**:

1. Given a selected car, When submitting an enquiry, Then all required fields are validated and stored locally.
2. Given a successful submission, When complete, Then the AI confirms receipt and next steps.

---

### User Story 6 - Shortlist (Priority: P2)

The user adds or removes cars from a shortlist accessible during the session. Shortlisted cars persist for the session and can be used to drive comparison or enquiry.

**Why this priority**: Supports exploration and delayed decision-making without losing context.

**Independent Test**: Add two cars to shortlist, revisit the shortlist, and verify they’re present and actionable (compare or enquire).

**Acceptance Scenarios**:

1. Given recommendations, When the user taps “Shortlist” on a car, Then the car appears in the session shortlist.
2. Given a shortlisted car, When removed, Then it no longer appears in the shortlist and dependent views update accordingly.

---

### User Story 7 - AI-Generated Customer Summary (Priority: P2)

The assistant generates a concise customer summary capturing purpose, budget, monthly expectation, fuel/transmission preferences, key concerns, cars viewed, selected car (if any), and readiness level.

**Why this priority**: Accelerates effective admin follow-up and continuity.

**Independent Test**: After a discovery session, request a summary and verify all required fields compile from the conversation and actions taken.

**Acceptance Scenarios**:

1. Given a completed discovery, When summary is requested/triggered, Then the assistant presents a structured summary with required fields.
2. Given missing inputs, When summarizing, Then the assistant flags gaps and suggests clarifying questions.

---

### User Story 8 - Admin Dashboard & Lead Status Flow (Priority: P2)

Admins view new enquiries, contact details, selected car, customer budget, finance estimate, AI-generated summary, cars recommended/compared, and can update lead status: New, Contacted, Interested, Finance discussion, Test drive requested, Closed, Lost.

**Why this priority**: Enables operational follow-up for demo leads.

**Independent Test**: Open the dashboard and verify a newly submitted enquiry appears with all required fields; update status and confirm persistence.

**Acceptance Scenarios**:

1. Given at least one enquiry, When opening the dashboard, Then the lead record shows all specified fields and initial status “New”.
2. Given a selected lead, When updating status, Then the new status persists and is visible on refresh.

---

### Edge Cases

- No matching cars after constraints tighten → assistant suggests relaxing specific filters and offers closest matches.
- CSV inventory has missing image path → show placeholder image and note the fallback.
- CSV row missing non-critical attribute → display available fields and mark missing as “N/A”.
- Conflicting preferences (e.g., very low budget + premium brand) → assistant explains trade-offs and offers alternatives.
- User changes preference repeatedly → ensure debounced refresh and consistent state; assistant summarizes what changed.
- Invalid enquiry inputs → show field-level validation messages and prevent submission until valid.
- Finance inputs extreme values → clamp to safe demo ranges and label as “example only”.

## Requirements (mandatory)

### Functional Requirements

- FR-001: System MUST conduct a conversational discovery to capture intent, budget, lifestyle, fuel, transmission, family size, mileage preference, and running cost expectation.
- FR-002: System MUST generate 1–3 explainable recommendations using only the local CSV inventory and linked local images.
- FR-003: Each recommendation MUST include an image, match score, finance estimate, and AI explanation mapping user inputs to vehicle attributes.
- FR-004: System MUST update recommendations live when preferences change and explain the impact.
- FR-005: System MUST support side-by-side comparison of 2–3 cars with required attributes (price, monthly estimate, mileage, fuel, transmission, body type, suitability, running cost indication, value-for-money explanation).
- FR-006: System MUST display finance details (price, deposit, term, example interest rate, estimated monthly) with an “indicative only, subject to approval” disclaimer.
- FR-007: System MUST provide a shortlist option to add/remove cars within the session.
- FR-008: System MUST capture enquiries with required fields and store them locally.
- FR-009: System MUST generate an AI-driven customer summary with all specified fields.
- FR-010: System MUST provide an admin dashboard listing enquiries and enabling lead status updates through the defined statuses.
- FR-011: System MUST maintain a persistent side assistant/chat during browsing, recommendations, comparison, finance view, and enquiry.
- FR-012: System MUST refresh comparison and shortlist views when underlying preferences or availability change.
- FR-013: System MUST clearly indicate when data is demo/sample and avoid implying real finance approval.
- FR-014: System MUST ingest a single CSV file for all required data located at data/dataset.csv; for MVP, parse per-row JSON blobs under columns named Car Inventory Data and Pricing Details to power recommendations and finance examples.
- FR-015: Until real images are provided, System MUST display a single standard dummy image for all vehicles in recommendations, details, comparison, and shortlist views.

### Key Entities

- Customer Session: discovery inputs, chat transcript, shortlist, comparison set, selected car.
- Inventory Vehicle: id, make, model, year, price, mileage, fuel, transmission, body type, monthly estimate, image path, description.
- Recommendation Card: vehicle ref, image, match score, finance estimate, explanation.
- Comparison Item: vehicle ref plus comparison attributes and suitability notes.
- Enquiry: customer details, selected car, budget, deposit, timeframe, contact preferences, timestamp, status.
- AI Customer Summary: purpose, budget, monthly expectation, fuel/transmission, key concerns, cars viewed, selected car, readiness.

## Success Criteria (mandatory)

### Measurable Outcomes

- SC-001: A first recommendation appears within 3 conversational turns after initial greeting on a typical CSV (≤200 rows).
- SC-002: Changing a single preference updates recommendations within 1 second (local run, mid-spec laptop).
- SC-003: 90% of demo users can compare 2 cars and reach an enquiry within 5 minutes.
- SC-004: 100% of finance displays include the indicative-only disclaimer.
- SC-005: First recommendations appear within 3 conversational turns after greeting using inputs of at least intent and monthly budget.
- SC-006: When preferences change, updated recommendations render within 1 second on a local machine (300ms debounce allowed).

## MVP Boundaries

- Runs fully on local machine; no external services.
- Uses only local CSV inventory and local image files (with placeholder fallback).
- Uses demo/sample data only; no real dealer, finance, or payment integrations.
- No credit check, finance submission, or production deployment.
- No authentication beyond what’s required for demo navigation.

## Out of Scope

- Real-time dealer inventory sync or VIN decoding.
- Real finance approval, eligibility checks, or credit scoring.
- Payment processing, trade-in valuation, or delivery scheduling.
- Multi-tenant admin, roles/permissions, or analytics beyond basic demo.
- Mobile apps or production-grade responsive tuning beyond a functional demo UI.

## Assumptions

- A single CSV file contains all necessary data at data/dataset.csv; each row includes JSON blobs labeled Car Inventory Data and Pricing Details. Other blobs (e.g., Match Score Logic, Rules) may be ignored in the MVP unless explicitly referenced.
- Vehicle images are not available at this stage; the UI will use one standard dummy image for all vehicles until images are supplied.
- Placeholder image path is defined in a JSON schema file at data/schema.json, with assets.placeholder_image set to assets/placeholder.svg.
- A simple, local persistence mechanism (e.g., file-based) is sufficient for storing enquiries.
- The AI assistant can access the CSV data in-memory for generating recommendations and explanations.
- Users have basic desktop browser access; no mobile optimization guarantees for MVP.

## Policies (Data and Behaviour)

- Match Score: Use provided total_match_score and threshold_passed when present; otherwise compute a 0–100 score with weights Budget (50%), Intent (30%), Lifestyle/Family (20%). Default display cutoff: 50/100.
- Match Score Tie‑breakers: When scores are equal, prefer (1) better budget fit, then (2) lower mileage, then (3) newer registration year, then (4) lower list price.
- Finance Defaults: If the user doesn’t set deposit/term/rate, use per-car values from Pricing Details. Canonical disclaimer: “All finance figures are examples only and subject to approval. No credit check is performed in this demo.”
- First Recommendations: Trigger after collecting intent and monthly budget (minimum). Always show up to 3 cars (initial and refreshed). If none meet criteria, show nearest alternatives and suggest relaxing constraints.
- Preference Changes: Apply a 300ms debounce to refresh; when no results remain, suggest targeted relaxations. Shortlist and comparison persist across changes; items that no longer fit are flagged accordingly.
	- Visibility for flagged items: display a clear “No longer fits” badge and a brief reason (e.g., “exceeds budget” or “fuel type changed”).
