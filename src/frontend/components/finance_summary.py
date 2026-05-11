from __future__ import annotations

import streamlit as st


def _format_currency(value: float | int | None) -> str:
    """Format a GBP amount without decimals for the finance summary UI."""
    amount = int(value) if value else 0
    return f"£{amount:,}"


def _format_term(term_months: int | None) -> str:
    """Format the finance term in months for display."""
    months = int(term_months) if term_months else 36
    return f"{months} months"


def finance_summary(
    monthly_budget: float | int | None,
    term_months: int | None,
    deposit: float | int | None,
) -> None:
    """Render a compact finance summary card for the recommendations panel."""
    st.markdown(
        f"""
        <div class="finance-summary" data-testid="finance-summary-card">
          <div class="finance-summary__icon" aria-hidden="true">💷</div>
          <div class="finance-summary__content">
            <div class="finance-summary__copy">
              <div class="finance-summary__label">Finance Summary</div>
              <p>Review your budget profile before exploring matching finance options.</p>
            </div>
            <div class="finance-summary__metrics" aria-label="Finance summary values">
              <div class="finance-summary__metric">
                <span>Monthly Budget</span>
                <strong>{_format_currency(monthly_budget)}</strong>
              </div>
              <div class="finance-summary__metric">
                <span>Term</span>
                <strong>{_format_term(term_months)}</strong>
              </div>
              <div class="finance-summary__metric">
                <span>Deposit</span>
                <strong>{_format_currency(deposit)}</strong>
              </div>
            </div>
          </div>
          <button class="finance-summary__button" type="button">View Finance Options</button>
        </div>
        """,
        unsafe_allow_html=True,
    )
