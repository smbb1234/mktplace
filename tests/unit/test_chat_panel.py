from __future__ import annotations

import importlib
import sys
import types

import pytest


class _FakeContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeStreamlit(types.SimpleNamespace):
    def __init__(self):
        super().__init__()
        self.session_state = {}

    def markdown(self, *args, **kwargs):
        return None

    def container(self):
        return _FakeContext()

    def columns(self, spec):
        count = spec if isinstance(spec, int) else len(spec)
        return [_FakeContext() for _ in range(count)]

    def button(self, *args, **kwargs):
        return False

    def text_input(self, *args, **kwargs):
        return ""


class _FakeBackendClient:
    def post_chat(self, payload):
        return {}


@pytest.fixture()
def chat_panel_module(monkeypatch):
    fake_st = _FakeStreamlit()
    fake_client_module = types.ModuleType("src.frontend.api_client.client")
    fake_client_module.BackendClient = lambda: _FakeBackendClient()

    monkeypatch.setitem(sys.modules, "streamlit", fake_st)
    monkeypatch.setitem(sys.modules, "src.frontend.api_client.client", fake_client_module)
    sys.modules.pop("src.frontend.state.session_state", None)
    sys.modules.pop("src.frontend.components.chat_panel", None)

    module = importlib.import_module("src.frontend.components.chat_panel")
    module.st.session_state.clear()
    return module


def test_initial_messages_exist(chat_panel_module):
    chat_panel_module._ensure_messages()

    messages = chat_panel_module.st.session_state["chat_messages"]
    assert [message["role"] for message in messages] == ["ai", "ai", "ai"]
    assert [message["text"] for message in messages] == [
        "Hi! I'm your AI car buying assistant.",
        "I'll help you find the perfect car that fits your needs and budget.",
        "To get started, what's your monthly budget for the car?",
    ]
    assert all("time" in message for message in messages)


def test_send_budget_appends_user_message(chat_panel_module):
    class Backend:
        def post_chat(self, payload):
            return {"monthly_budget": 450}

    chat_panel_module._send_message("$450 per month", "sess-1", backend_client=Backend())

    messages = chat_panel_module.st.session_state["chat_messages"]
    assert any(
        message["role"] == "user" and message["text"] == "$450 per month"
        for message in messages
    )


def test_post_chat_preferences_are_written_to_state(chat_panel_module):
    class Backend:
        def post_chat(self, payload):
            return {"preferences": {"monthly_budget": 500, "fuel_type": "Petrol"}}

    chat_panel_module._send_message("Budget is 500 and petrol", "sess-1", backend_client=Backend())

    assert chat_panel_module.st.session_state["preferences"] == {
        "monthly_budget": 500,
        "fuel_type": "Petrol",
    }


def test_next_ai_message_asks_correct_next_question(chat_panel_module):
    assert (
        chat_panel_module._next_ai_message({})["text"]
        == "What's your monthly budget for the car?"
    )

    fuel_message = chat_panel_module._next_ai_message({"monthly_budget": 400})
    assert fuel_message["text"] == "Great — what fuel type would you prefer?"
    assert fuel_message["quick_replies"] == ["Petrol", "Diesel", "Hybrid / Electric"]

    transmission_message = chat_panel_module._next_ai_message(
        {"monthly_budget": 400, "fuel_type": "Diesel"}
    )
    assert (
        transmission_message["text"]
        == "Got it. Would you prefer automatic or manual transmission?"
    )
    assert transmission_message["quick_replies"] == ["Automatic", "Manual"]

    done_message = chat_panel_module._next_ai_message(
        {"monthly_budget": 400, "fuel_type": "Diesel", "transmission": "Manual"}
    )
    assert "generating recommendations" in done_message["text"]


def test_quick_reply_uses_send_message_logic(chat_panel_module, monkeypatch):
    calls = []

    def fake_send_message(txt, session_id=None):
        calls.append((txt, session_id))

    monkeypatch.setattr(chat_panel_module, "_send_message", fake_send_message)

    chat_panel_module._send_quick_reply("Hybrid / Electric", "sess-quick")

    assert calls == [("Hybrid / Electric", "sess-quick")]
