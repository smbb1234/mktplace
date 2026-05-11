from __future__ import annotations

import streamlit as st
from typing import List


def comparison_view(items: List[dict]):
    st.header("Comparison")
    if not items:
        st.info("No vehicles selected for comparison")
        return
    cols = st.columns(len(items))
    for i, v in enumerate(items):
        with cols[i]:
            st.subheader(v.get("make", "") + " " + (v.get("model") or ""))
            st.write(f"Price: {v.get('pricing', {}).get('list_price_gbp')}")
            st.write(f"Monthly: {v.get('pricing', {}).get('monthly_from_gbp')}")
            st.write(f"Mileage: {v.get('mileage')}")
