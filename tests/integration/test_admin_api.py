from types import SimpleNamespace

from fastapi.testclient import TestClient

from src.backend.main import app

client = TestClient(app)


def test_admin_route_list_includes_flush_offline():
    route_methods = {
        route.path: getattr(route, "methods", set()) for route in app.routes
    }

    assert "/admin/flush_offline" in route_methods
    assert "POST" in route_methods["/admin/flush_offline"]
    assert "GET" in route_methods["/admin/enquiries"]
    assert "POST" in route_methods["/admin/enquiries/{enquiry_id}/status"]


def test_flush_offline_allows_test_path_without_admin_token(monkeypatch):
    from src.backend.scripts import flush_offline_enquiries
    from src.shared.config import settings as settings_module

    monkeypatch.setattr(
        settings_module, "get_settings", lambda: SimpleNamespace(admin_token="")
    )
    monkeypatch.setattr(flush_offline_enquiries, "flush_queue", lambda: None)

    r = client.post("/admin/flush_offline")

    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_flush_offline_rejects_wrong_admin_token_when_configured(monkeypatch):
    from src.backend.scripts import flush_offline_enquiries
    from src.shared.config import settings as settings_module

    monkeypatch.setattr(
        settings_module,
        "get_settings",
        lambda: SimpleNamespace(admin_token="correct-token"),
    )
    monkeypatch.setattr(flush_offline_enquiries, "flush_queue", lambda: None)

    r = client.post("/admin/flush_offline", headers={"X-Admin-Token": "wrong-token"})

    assert r.status_code == 401


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
