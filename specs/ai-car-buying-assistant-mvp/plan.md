# Implementation Plan: AI Car Buying Assistant MVP

**Branch**: `feature/20260508-ai-car-buying-assistant-mvp` | **Date**: 2026-05-08 | **Spec**: [specs/ai-car-buying-assistant-mvp/spec.md](specs/ai-car-buying-assistant-mvp/spec.md)
**Input**: Feature specification from `/specs/ai-car-buying-assistant-mvp/spec.md`

**Note**: This plan intentionally avoids technical design choices (frameworks, architecture) per MVP constraints. It focuses on sequencing, gates, and deliverable scope.

## Summary

Advisor-led journey that welcomes the customer, runs a short discovery to capture intent and monthly budget (minimum), then presents 1–3 explainable recommendations from a local CSV with a placeholder image. Users can refine preferences live (debounced), compare 2–3 cars, view indicative-only finance, shortlist, submit an enquiry, and the admin can review leads and update statuses. Policies define match score scale/weights, tie-breakers, finance defaults + disclaimer, recommendation trigger and caps, and persistence behavior for shortlist/comparison.

## Technical Context

- Language/Version: [NEEDS CLARIFICATION]
- Primary Dependencies: [NEEDS CLARIFICATION]
- Storage: Local files only (CSV inventory, local placeholder image, local enquiry storage) — exact mechanism [NEEDS CLARIFICATION]
- Testing: [NEEDS CLARIFICATION]
- Target Platform: Desktop browser (local run) — implementation details [NEEDS CLARIFICATION]
- Project Type: [NEEDS CLARIFICATION]
- Performance Goals: SC-001 (≤3 turns to first rec), SC-002/SC-006 (≤1s refresh locally)
- Constraints: Local-only, demo data, no real integrations
- Scale/Scope: Small demo dataset (e.g., ≤200 rows)

## Constitution Check

GATE: Must pass before Phase 0 research/design.

- Agent-led interactive buying experience upheld (AI discovery, iterative refinement)
- Explainable recommendations with match score, finance estimate, and rationale
- Visual recommendation workspace + persistent side assistant
- Finance safety: indicative-only wording; no credit checks or real submissions
- Local-only MVP: CSV inventory, placeholder images, demo data
- Out-of-scope honored: no dealer/finance/payment integrations; no production deployment

## Project Structure

### Documentation (this feature)

```text
specs/ai-car-buying-assistant-mvp/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Single-project layout consistent with repo; exact module breakdown to be refined post-clarifications and Constitution Check.

## Complexity Tracking

> Fill ONLY if Constitution Check has violations that must be justified.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| — | — | — |
