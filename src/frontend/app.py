from __future__ import annotations

import os

import pandas as pd
import requests
import streamlit as st

from src.shared.config.settings import get_settings

st.set_page_config(page_title="AI Car Buying Assistant", page_icon="🚗", layout="wide")

settings = get_settings()

backend_host = os.getenv("BACKEND_HOST", "backend")
backend_port = os.getenv("BACKEND_PORT", str(settings.fastapi_port))
backend_base = f"http://{backend_host}:{backend_port}"

st.title("🚗 AI Car Buying Assistant (MVP)")

# Health check section
with st.sidebar:
    st.header("Status")
    try:
        r = requests.get(f"{backend_base}/health", timeout=5)
        if r.ok:
            st.success("Backend: healthy")
        else:
            st.warning(f"Backend: {r.status_code}")
    except Exception as e:
        st.error(f"Backend unreachable: {e}")

# Inventory preview
st.subheader("Inventory snapshot")
try:
    csv_path = str(settings.inventory_csv_path)
    df = pd.read_csv(csv_path)
    st.caption(f"Loaded inventory from {csv_path}")
    st.dataframe(df.head(10))
except Exception as e:
    st.warning(f"Unable to load inventory CSV: {e}")

st.info("This is a minimal Streamlit shell wired for Docker Compose dev. UI features will grow iteratively.")
