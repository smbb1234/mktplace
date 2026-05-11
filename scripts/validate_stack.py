#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from contextlib import closing
from typing import Callable


def load_env():
    # Load from .env.docker for credentials only; override host/port for host access.
    env_path = os.path.join(os.getcwd(), ".env.docker")
    env = {}
    if os.path.exists(env_path):
        from dotenv import dotenv_values

        env = dotenv_values(env_path)
    # Ensure sensible defaults.
    env.setdefault("POSTGRES_DB", "car_mvp")
    env.setdefault("POSTGRES_USER", "car_user")
    env.setdefault("POSTGRES_PASSWORD", "car_password")
    # Force host access (localhost:5433) regardless of container values.
    env["POSTGRES_HOST"] = os.environ.get("POSTGRES_HOST", "localhost")
    env["POSTGRES_PORT"] = os.environ.get("POSTGRES_PORT", "5433")
    return env


def _session(timeout=5.0):
    import requests
    from requests.adapters import HTTPAdapter, Retry

    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.timeout = timeout
    return s


def wait_for_http(
    url: str,
    timeout_s: int = 60,
    verify_ssl: bool = True,
    expect_json: bool | None = None,
):
    s = _session()
    start = time.time()
    last_err = None
    while time.time() - start < timeout_s:
        try:
            resp = s.get(url, timeout=s.timeout, verify=verify_ssl)
            if expect_json is True:
                resp.json()
            if 200 <= resp.status_code < 500:
                return resp
        except Exception as e:  # noqa: BLE001 - report the last wait failure to users.
            last_err = e
        time.sleep(1.0)
    raise RuntimeError(f"HTTP wait timed out for {url}: {last_err}")


def check_backend_health() -> dict:
    url = os.environ.get("BACKEND_HEALTH_URL", "http://localhost:8000/health")
    resp = wait_for_http(url, timeout_s=90, verify_ssl=True, expect_json=True)
    data = resp.json()
    ok = isinstance(data, dict) and data.get("status") == "ok"
    return {"service": "backend", "url": url, "ok": ok, "data": data}


def check_streamlit() -> dict:
    url = os.environ.get("FRONTEND_URL", "http://localhost:8501/")
    resp = wait_for_http(url, timeout_s=120, verify_ssl=True)
    ok = resp.status_code in (200, 302)
    return {"service": "frontend", "url": url, "ok": ok, "status_code": resp.status_code}


def check_portainer() -> dict:
    url = os.environ.get("PORTAINER_URL", "https://localhost:9443/")
    # Portainer uses a self-signed cert by default; disable verification.
    resp = wait_for_http(url, timeout_s=60, verify_ssl=False)
    ok = resp.status_code in (200, 302, 401)
    return {"service": "portainer", "url": url, "ok": ok, "status_code": resp.status_code}


def check_chroma() -> dict:
    base = os.environ.get("CHROMA_URL", "http://localhost:8001")
    for path in ("/api/v1/heartbeat", "/api/v1", "/api/health", "/"):
        url = base + path
        try:
            # Allow longer warmup for Chroma.
            resp = wait_for_http(url, timeout_s=120)
            ok = 200 <= resp.status_code < 400
            try:
                data = resp.json()
            except Exception:  # noqa: BLE001 - response body is diagnostic only.
                data = {"body": resp.text[:256]}
            if ok:
                return {
                    "service": "chroma",
                    "url": url,
                    "ok": ok,
                    "status_code": resp.status_code,
                    "data": data,
                }
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
            import psycopg

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
        except Exception as e:  # noqa: BLE001 - report connection retries to users.
            last_err = e
            time.sleep(1.5)
    return {"service": "postgres", "ok": False, "error": str(last_err)}


def _check_definitions() -> dict[str, Callable[[], dict]]:
    return {
        "postgres": check_postgres_crud,
        "backend": check_backend_health,
        "frontend": check_streamlit,
        "chroma": check_chroma,
        "portainer": check_portainer,
    }


def _selected_checks(args: argparse.Namespace) -> list[str]:
    available = _check_definitions()
    if args.only:
        return args.only

    checks = ["postgres", "backend", "chroma"]
    if args.include_frontend:
        checks.append("frontend")
    if args.include_portainer:
        checks.append("portainer")
    return [name for name in checks if name in available]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Docker Compose services without requiring local Streamlit unless requested."
    )
    parser.add_argument(
        "--include-frontend",
        action="store_true",
        help="Also validate Streamlit on FRONTEND_URL (default: http://localhost:8501/).",
    )
    parser.add_argument(
        "--include-portainer",
        action="store_true",
        help="Also validate Portainer on PORTAINER_URL (default: https://localhost:9443/).",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        choices=sorted(_check_definitions().keys()),
        help="Run only the named service checks.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    checks = _check_definitions()
    selected = _selected_checks(args)
    print(f"\n=== Docker stack health check: {', '.join(selected)} ===")

    results = []
    overall_ok = True
    for name in selected:
        print(f"--- Checking {name} ---")
        try:
            res = checks[name]()
        except Exception as exc:  # noqa: BLE001 - convert check exceptions into clear failures.
            res = {"service": name, "ok": False, "error": str(exc)}
        results.append(res)
        overall_ok = overall_ok and res.get("ok", False)
        status = "OK" if res.get("ok") else "FAIL"
        print(f"[ {status} ] {res.get('service')} -> {json.dumps(res, default=str)}")

    if not overall_ok:
        failed = [res.get("service", "unknown") for res in results if not res.get("ok")]
        print(f"Docker stack validation failed for: {', '.join(failed)}", file=sys.stderr)
        sys.exit(1)
    print("All selected services validated successfully.")


if __name__ == "__main__":
    main()
