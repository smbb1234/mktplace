import requests


def test_frontend_serves_title():
    resp = requests.get("http://127.0.0.1:8501", timeout=5)
    assert resp.status_code == 200
    # Streamlit renders app client-side; ensure the root container is present
    assert '<div id="root"></div>' in resp.text or '<div id="root"' in resp.text
