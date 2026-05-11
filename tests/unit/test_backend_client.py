from __future__ import annotations

import importlib
import sys
import types


def test_create_enquiry_posts_payload_to_enquiries_endpoint(monkeypatch):
    calls = []
    expected_response = object()
    fake_requests = types.SimpleNamespace()

    def fake_post(url, json):
        calls.append((url, json))
        return expected_response

    fake_requests.post = fake_post
    fake_requests.get = lambda *args, **kwargs: None
    fake_settings_module = types.ModuleType("src.shared.config.settings")
    fake_settings_module.get_settings = lambda: types.SimpleNamespace(
        fastapi_host="localhost",
        fastapi_port=8000,
    )

    monkeypatch.setitem(sys.modules, "requests", fake_requests)
    monkeypatch.setitem(sys.modules, "src.shared.config.settings", fake_settings_module)
    sys.modules.pop("src.frontend.api_client.client", None)

    client_module = importlib.import_module("src.frontend.api_client.client")
    client = client_module.BackendClient(base_url="http://backend.test")
    payload = {"vehicle_id": "veh-1", "full_name": "Ada"}

    response = client.create_enquiry(payload)

    assert response is expected_response
    assert calls == [("http://backend.test/enquiries/", payload)]
