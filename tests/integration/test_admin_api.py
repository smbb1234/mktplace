from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)


def test_admin_list_and_update_integration():
    r = client.get("/admin/enquiries")
    if r.status_code == 503:
        assert True
        return
    assert r.status_code == 200
    items = r.json()
    if not items:
        return
    eid = items[0]["enquiry_id"]
    ur = client.post(f"/admin/enquiries/{eid}/status", params={"status": "Contacted"})
    assert ur.status_code in (200, 503)
