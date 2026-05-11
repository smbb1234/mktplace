from __future__ import annotations

import streamlit as st


def summary_cards(budget: float | None, term: int | None, deposit: float | None):
    cols = st.columns(3)
    with cols[0]:
        st.markdown(
            f"""
            <div class='card' style='padding:16px;'>
              <div style='font-size:13px;color:#6b7a90;'>Monthly Budget</div>
              <div style='font-size:24px;font-weight:700;'>£{int(budget) if budget else 0}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            f"""
            <div class='card' style='padding:16px;'>
              <div style='font-size:13px;color:#6b7a90;'>Finance Term</div>
              <div style='font-size:24px;font-weight:700;'>{int(term) if term else 36} months</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.markdown(
            f"""
            <div class='card' style='padding:16px;'>
              <div style='font-size:13px;color:#6b7a90;'>Initial Deposit</div>
              <div style='font-size:24px;font-weight:700;'>£{int(deposit) if deposit else 1000}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
