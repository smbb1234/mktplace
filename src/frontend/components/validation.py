from __future__ import annotations

import streamlit as st


def require_field(value, name: str):
    if not value:
        st.error(f"{name} is required")
        return False
    return True


def validate_enquiry_form(data: dict) -> bool:
    ok = True
    ok &= require_field(data.get("full_name"), "Full name")
    ok &= require_field(data.get("email"), "Email")
    ok &= require_field(data.get("phone"), "Phone")
    ok &= require_field(data.get("vehicle_id"), "Vehicle ID")
    return bool(ok)
