from __future__ import annotations

import importlib
import sys
import types
from dataclasses import dataclass

import pytest


class _FakeStreamlit(types.SimpleNamespace):
    def __init__(self):
        super().__init__()
        self.success_messages: list[str] = []
        self.error_messages: list[str] = []
        self.button_clicked = True
        self.inputs = {
            "Vehicle ID": "veh-123",
            "Full name": "Ada Lovelace",
            "Email": "ada@example.com",
            "Phone": "07123456789",
        }

    def header(self, *args, **kwargs):
        return None

    def text_input(self, label, value="", **kwargs):
        if label == "Vehicle ID" and value:
            return value
        return self.inputs.get(label, value)

    def number_input(self, label, value=0, **kwargs):
        return 500 if label == "Monthly budget" else 1000

    def selectbox(self, label, options, **kwargs):
        return options[0]

    def button(self, *args, **kwargs):
        return self.button_clicked

    def success(self, message):
        self.success_messages.append(message)

    def error(self, message):
        self.error_messages.append(message)


@dataclass
class _FakeResponse:
    status_code: int


class _FakeBackendClient:
    def __init__(self, status_code=201):
        self.status_code = status_code
        self.payloads: list[dict] = []

    def create_enquiry(self, payload: dict):
        self.payloads.append(payload)
        return _FakeResponse(self.status_code)


@pytest.fixture()
def enquiry_form_module(monkeypatch):
    fake_st = _FakeStreamlit()
    fake_client = _FakeBackendClient()
    fake_client_module = types.ModuleType("src.frontend.api_client.client")
    fake_client_module.BackendClient = lambda: fake_client

    monkeypatch.setitem(sys.modules, "streamlit", fake_st)
    monkeypatch.setitem(sys.modules, "src.frontend.api_client.client", fake_client_module)
    sys.modules.pop("src.frontend.components.validation", None)
    sys.modules.pop("src.frontend.components.enquiry_form", None)

    module = importlib.import_module("src.frontend.components.enquiry_form")
    module.client = fake_client
    return module, fake_st, fake_client


def test_enquiry_form_submits_via_backend_client_create_enquiry(enquiry_form_module):
    module, fake_st, fake_client = enquiry_form_module

    module.enquiry_form(default_vehicle_id="veh-456")

    assert fake_client.payloads == [
        {
            "vehicle_id": "veh-456",
            "full_name": "Ada Lovelace",
            "email": "ada@example.com",
            "phone": "07123456789",
            "monthly_budget_gbp": 500,
            "deposit_gbp": 1000,
            "buying_timeframe": "ASAP",
        }
    ]
    assert fake_st.success_messages == ["提交成功。"]
    assert fake_st.error_messages == []


def test_enquiry_form_accepted_response_shows_queued_message(enquiry_form_module):
    module, fake_st, fake_client = enquiry_form_module
    fake_client.status_code = 202

    module.enquiry_form(default_vehicle_id="veh-456")

    assert fake_client.payloads
    assert fake_st.success_messages == ["已接收，稍后同步。"]
    assert any(term in fake_st.success_messages[0] for term in ["已接收", "同步"])
