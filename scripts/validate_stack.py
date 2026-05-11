#!/usr/bin/env python3
import os
import sys
import time
import json
import ssl
from contextlib import closing

import requests
from requests.adapters import HTTPAdapter, Retry
from dotenv import dotenv_values
import psycopg


def load_env():
    # Load from .env.docker for credentials only; override host/port for host access
    env_path = os.path.join(os.getcwd(), ".env.docker")
    env = {}
    if os.path.exists(env_path):
        env = dotenv_values(env_path)
    # Ensure sensible defaults
    env.setdefault("POSTGRES_DB", "car_mvp")
    env.setdefault("POSTGRES_USER", "car_user")
    env.setdefault("POSTGRES_PASSWORD", "car_password")
    # Force host access (localhost:5433) regardless of container values
    env["POSTGRES_HOST"] = "localhost"
    env["POSTGRES_PORT"] = "5433"
    return env


def _session(timeout=5.0):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.timeout = timeout
    return s


def wait_for_http(url: str, timeout_s: int = 60, verify_ssl: bool = True, expect_json: bool | None = None):
    s = _session()
    start = time.time()
    last_err = None
    while time.time() - start < timeout_s:
        try:
            resp = s.get(url, verify=verify_ssl)
            if expect_json is True:
                resp.json()
            if 200 <= resp.status_code < 500:
                return resp
        except Exception as e:
            last_err = e
        time.sleep(1.0)
    raise RuntimeError(f"HTTP wait timed out for {url}: {last_err}")


def check_backend_health() -> dict:
    url = "http://localhost:8000/health"
    resp = wait_for_http(url, timeout_s=90, verify_ssl=True, expect_json=True)
    data = resp.json()
    ok = isinstance(data, dict) and data.get("status") == "ok"
    return {"service": "backend", "url": url, "ok": ok, "data": data}


def check_streamlit() -> dict:
    url = "http://localhost:8501/"
    resp = wait_for_http(url, timeout_s=120, verify_ssl=True)
    ok = resp.status_code in (200, 302)
    return {"service": "frontend", "url": url, "ok": ok, "status_code": resp.status_code}


def check_portainer() -> dict:
    url = "https://localhost:9443/"
    try:
        # Portainer uses a self-signed cert by default; disable verification
        resp = wait_for_http(url, timeout_s=60, verify_ssl=False)
        ok = resp.status_code in (200, 302, 401)
        return {"service": "portainer", "url": url, "ok": ok, "status_code": resp.status_code}
    except Exception as e:
        return {"service": "portainer", "url": url, "ok": False, "error": str(e)}


def check_chroma() -> dict:
    # Try heartbeat endpoint first
    base = "http://localhost:8001"
    for path in ("/api/v1/heartbeat", "/api/v1", "/"):
        url = base + path
        try:
            resp = wait_for_http(url, timeout_s=60)
            # Any 200/JSON is acceptable as proof of life
            ok = 200 <= resp.status_code < 400
            try:
                data = resp.json()
            except Exception:
                data = {"body": resp.text[:256]}
            if ok:
                return {"service": "chroma", "url": url, "ok": ok, "status_code": resp.status_code, "data": data}
        except Exception:
            continue
    return {"service": "chroma", "url": base, "ok": False, "error": "No heartbeat response"}


def check_postgres_crud() -> dict:
    env = load_env()
    dsn = (
        f"host={env['POSTGRES_HOST']} port={env['POSTGRES_PORT']} dbname={env['POSTGRES_DB']} "
        f"user={env['POSTGRES_USER']} password={env['POSTGRES_PASSWORD']}"
    )

    start = time.time()
    last_err = None
    while time.time() - start < 90:
        try:
            with closing(psycopg.connect(dsn, autocommit=True)) as conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE TABLE IF NOT EXISTS connectivity_test (id SERIAL PRIMARY KEY, note TEXT)")
                    cur.execute("INSERT INTO connectivity_test (note) VALUES (%s) RETURNING id", ("hello",))
                    inserted_id = cur.fetchone()[0]
                    cur.execute("SELECT note FROM connectivity_test WHERE id=%s", (inserted_id,))
                    note = cur.fetchone()[0]
                    cur.execute("DROP TABLE connectivity_test")
                    ok = note == "hello"
                    return {"service": "postgres", "ok": ok, "details": {"inserted_id": inserted_id, "note": note}}
        except Exception as e:
            last_err = e
            time.sleep(1.5)
    return {"service": "postgres", "ok": False, "error": str(last_err)}


def main():
    checks = [
        check_postgres_crud,
        check_backend_health,
        check_streamlit,
        check_chroma,
        check_portainer,
    ]
    results = []
    overall_ok = True
    for fn in checks:
        res = fn()
        results.append(res)
        overall_ok = overall_ok and res.get("ok", False)
        status = "OK" if res.get("ok") else "FAIL"
        print(f"[ {status} ] {res.get('service')} -> {json.dumps(res, default=str)}")
    if not overall_ok:
        print("One or more services failed validation", file=sys.stderr)
        sys.exit(1)
    print("All services validated successfully.")


if __name__ == "__main__":
    main()
