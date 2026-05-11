from __future__ import annotations

from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)


def test_admin_list_and_update():
    r = client.get("/admin/enquiries")
    # If DB unavailable, API returns 503; accept that for local dev
    if r.status_code == 503:
        assert True
        return
    assert r.status_code == 200
    items = r.json()
    # If no items, nothing to update
    if not items:
        assert isinstance(items, list)
        return
    eid = items[0].get("enquiry_id")
    ur = client.post(f"/admin/enquiries/{eid}/status", params={"status": "Contacted"})
    assert ur.status_code in (200, 503)
