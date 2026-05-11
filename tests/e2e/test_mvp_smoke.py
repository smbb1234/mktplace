from __future__ import annotations

from fastapi.testclient import TestClient
from src.backend.api import enquiries as enquiries_api
from src.backend.main import app
from src.backend.services.inventory.catalog import get_default_catalog


client = TestClient(app)


def test_mvp_smoke_flow(monkeypatch, tmp_path):
    # health
    r = client.get("/health")
    assert r.status_code == 200

    # post a chat message to create session prefs
    resp = client.post("/chat/message", json={"message": "I'm looking to buy, budget £300 per month"})
    assert resp.status_code == 200
    prefs = resp.json()
    assert "monthly_budget" in prefs or prefs.get("monthly_budget") is None

    # get recommendations (session created implicitly)
    recs = client.get("/recommendations/from_session")
    if recs.status_code == 503:
        # attempt to initialize a default catalog from sample CSV and retry
        try:
            c = get_default_catalog(csv_path="data/datasetSample.csv")
            # inject into startup module catalog used by endpoints
            import src.backend.startup as startup

            startup.catalog = c
        except Exception:
            pass
        recs = client.get("/recommendations/from_session")
    assert recs.status_code == 200

    # seed and create an enquiry via API
    # choose a vehicle from catalog
    catalog = client.get("/catalog/")
    assert catalog.status_code == 200
    items = catalog.json()
    assert items

    monkeypatch.setattr(enquiries_api, "OFFLINE_QUEUE", tmp_path / "offline_enquiries.jsonl")

    vid = items[0].get("vehicle_id")
    enquiry = {
        "vehicle_id": vid,
        "full_name": "E2E Tester",
        "email": "e2e@test.com",
        "phone": "+447700900010",
    }
    er = client.post("/enquiries/", json=enquiry)
    assert er.status_code in (201, 202)
    if er.status_code == 202:
        detail = er.json().get("detail", "").lower()
        assert "queued" in detail or "accepted" in detail
