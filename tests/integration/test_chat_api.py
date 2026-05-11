from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.backend.main import app
from src.backend.services.ai import conversation_orchestrator

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_chat_sessions():
    conversation_orchestrator._SESSIONS.clear()
    yield
    conversation_orchestrator._SESSIONS.clear()


def test_post_chat_message_extracts_budget_and_returns_response_contract():
    response = client.post(
        "/chat/message",
        json={"message": "I'm looking to buy with a budget of £450 per month"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["reply"]
    assert body["session_id"]
    assert body["intent"] == "purchase"
    assert body["monthly_budget"] == 450
    assert "fuel_type" in body
    assert "transmission" in body
    assert "family_size" in body


def test_post_chat_message_extracts_fuel_type_on_existing_session():
    first = client.post("/chat/message", json={"message": "budget £500 per month"})
    session_id = first.json()["session_id"]

    response = client.post(
        "/chat/message",
        json={"session_id": session_id, "message": "I prefer diesel cars"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["reply"]
    assert body["session_id"] == session_id
    assert body["monthly_budget"] == 500
    assert body["fuel_type"] == "Diesel"
    assert "transmission" in body


def test_post_chat_message_extracts_transmission_on_existing_session():
    first = client.post(
        "/chat/message",
        json={"message": "budget £500 per month and petrol please"},
    )
    session_id = first.json()["session_id"]

    response = client.post(
        "/chat/message",
        json={"session_id": session_id, "message": "automatic transmission"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["reply"]
    assert body["session_id"] == session_id
    assert body["monthly_budget"] == 500
    assert body["fuel_type"] == "Petrol"
    assert body["transmission"] == "Automatic"
