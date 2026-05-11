from __future__ import annotations

import streamlit as st


def summary_cards(budget: float | None, term: int | None, deposit: float | None):
    st.markdown("<div class='summary-cards'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='summary-small'>
          <div style='font-size:13px;color:#4F6690;'>Monthly Budget</div>
          <div style='font-size:22px;font-weight:700;'>£{int(budget) if budget else 0}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class='summary-small'>
          <div style='font-size:13px;color:#4F6690;'>36 Months Term</div>
          <div style='font-size:22px;font-weight:700;'>{int(term) if term else 36} months</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class='summary-small'>
          <div style='font-size:13px;color:#4F6690;'>Initial Deposit</div>
          <div style='font-size:22px;font-weight:700;'>£{int(deposit) if deposit else 1000}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
