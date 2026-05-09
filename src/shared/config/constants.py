"""Shared constants for the AI Car Buying Assistant MVP."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INVENTORY_CSV_PATH = PROJECT_ROOT / "data" / "dataset.csv"
DEFAULT_PLACEHOLDER_IMAGE_PATH = PROJECT_ROOT / "assets" / "placeholder.svg"

FINANCE_DISCLAIMER = (
    "All finance figures are examples only and subject to approval. "
    "No credit check is performed in this demo."
)

MATCH_SCORE_CUTOFF = 50
MATCH_SCORE_WEIGHTS = {
    "budget": 0.5,
    "intent": 0.3,
    "lifestyle_family": 0.2,
}

MIN_RECOMMENDATION_INPUTS = ("intent", "monthly_budget")
RECOMMENDATION_WINDOW_TURNS = 3
PREFERENCE_REFRESH_DEBOUNCE_MS = 300

ALLOWED_LEAD_STATUSES = (
    "New",
    "Contacted",
    "Interested",
    "Finance discussion",
    "Test drive requested",
    "Closed",
    "Lost",
)