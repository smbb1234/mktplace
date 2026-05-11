from __future__ import annotations

from typing import Any

import streamlit as st

DEFAULT_MONTHLY_BUDGET = 0
DEFAULT_TERM_MONTHS = 36
DEFAULT_DEPOSIT = 0


def _coerce_int(value: Any, default: int) -> int:
    if value is None:
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _session_value(key: str, default: Any = None) -> Any:
    value = st.session_state.get(key, default)
    return default if value is None else value


def _preference_value(key: str, default: Any = None) -> Any:
    preferences = st.session_state.get("preferences", {})
    if not isinstance(preferences, dict):
        return default
    value = preferences.get(key, default)
    return default if value is None else value


def summary_cards(
    monthly_budget: float | int | None = None,
    term_months: int | None = None,
    deposit: float | int | None = None,
) -> None:
    resolved_monthly_budget = _coerce_int(
        _preference_value("monthly_budget", monthly_budget), DEFAULT_MONTHLY_BUDGET
    )
    resolved_term_months = _coerce_int(
        _session_value("finance_term", term_months), DEFAULT_TERM_MONTHS
    )
    resolved_deposit = _coerce_int(
        _session_value("finance_deposit", deposit), DEFAULT_DEPOSIT
    )

    st.markdown("<div class='summary-cards'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='summary-small'>
          <div style='font-size:22px;font-weight:700;'>£{resolved_monthly_budget} Monthly Budget</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class='summary-small'>
          <div style='font-size:22px;font-weight:700;'>{resolved_term_months} Months Term</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class='summary-small'>
          <div style='font-size:22px;font-weight:700;'>£{resolved_deposit} Initial Deposit</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
