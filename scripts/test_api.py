#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys


def safe_json(resp):
    try:
        return resp.json()
    except Exception:
        print(f"REQUEST FAILED: status={resp.status_code}", file=sys.stderr)
        print(f"BODY:\n{resp.text}", file=sys.stderr)
        return None


def print_stage(name: str) -> None:
    print(f"\n=== API smoke: {name} ===")


def request_or_fail(method: str, url: str, **kwargs):
    import requests

    try:
        response = requests.request(method, url, timeout=kwargs.pop("timeout", 10), **kwargs)
    except requests.RequestException as exc:
        raise RuntimeError(f"{method} {url} failed to connect: {exc}") from exc
    if response.status_code >= 500:
        raise RuntimeError(f"{method} {url} returned {response.status_code}: {response.text[:500]}")
    return response


def run(base_url: str) -> None:
    base = base_url.rstrip("/")

    print_stage("health")
    health = request_or_fail("GET", f"{base}/health")
    health_payload = safe_json(health)
    print(json.dumps(health_payload, indent=2, default=str))
    if health.status_code != 200 or not isinstance(health_payload, dict) or health_payload.get("status") != "ok":
        raise RuntimeError(f"Health check failed with status {health.status_code}: {health_payload}")

    print_stage("catalog")
    catalog = request_or_fail("GET", f"{base}/catalog")
    catalog_payload = safe_json(catalog) or []
    if catalog.status_code != 200 or not isinstance(catalog_payload, list):
        raise RuntimeError(f"Catalog check failed with status {catalog.status_code}: {catalog_payload}")
    print(json.dumps(catalog_payload[:2], indent=2, default=str))

    print_stage("enquiry create")
    enquiry = request_or_fail(
        "POST",
        f"{base}/enquiries",
        json={
            "vehicle_id": "CAR-2026-0001",
            "full_name": "T Tester",
            "email": "t@t.com",
            "phone": "000",
        },
    )
    enquiry_payload = safe_json(enquiry)
    print(json.dumps(enquiry_payload, indent=2, default=str))
    if enquiry.status_code not in (200, 201):
        raise RuntimeError(f"Enquiry check failed with status {enquiry.status_code}: {enquiry_payload}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a backend API smoke test against a running service.")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Backend base URL.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        run(args.base_url)
    except Exception as exc:  # noqa: BLE001 - top-level script should show a concise failure reason.
        print(f"API smoke failed: {exc}", file=sys.stderr)
        return 1
    print("\nAPI smoke completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
