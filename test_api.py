#!/usr/bin/env python3
"""
Simple backend connectivity tester.

Usage:
  python test_api.py [BASE_URL]

Defaults to BASE_URL from env, or http://localhost:7860.

Examples:
  BASE_URL=https://<your-space>.hf.space python test_api.py
  python test_api.py http://localhost:7860
"""

import os
import sys
import json
from typing import Any, Optional

import requests


def pick_base_url() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1].rstrip("/")
    env = os.getenv("BASE_URL")
    if env:
        return env.rstrip("/")
    return "http://localhost:7860"


def dump_response(r: requests.Response, label: str) -> None:
    print(f"\n=== {label} ===")
    print(f"URL: {r.request.method} {r.url}")
    print(f"Status: {r.status_code} {r.reason}")
    ctype = r.headers.get("Content-Type", "<none>")
    print(f"Content-Type: {ctype}")
    try:
        if "application/json" in ctype:
            parsed: Any = r.json()
            print("Body (JSON):")
            print(json.dumps(parsed, indent=2)[:2000])
        else:
            print("Body (text):")
            print((r.text or "")[:1000])
    except Exception as e:
        print(f"[warn] Failed to parse body: {e}")


def hit(session: requests.Session, base: str, path: str, label: Optional[str] = None):
    url = f"{base}{path}"
    r = session.get(url, timeout=20)
    dump_response(r, label or path)
    return r


def main():
    base = pick_base_url()
    print(f"[info] Testing base URL: {base}")

    # In some managed platforms, SSL verification may require full chain.
    # Leave verify=True by default; allow override if needed.
    verify = os.getenv("REQUESTS_VERIFY", "true").lower() not in ("0", "false", "no")

    with requests.Session() as s:
        s.verify = verify

        # Health check
        hit(s, base, "/api/hello", "Health check /api/hello")

        # OpenAPI docs landing
        hit(s, base, "/api/docs", "Docs /api/docs (should be HTML)")

        # Sample data endpoint
        hit(s, base, "/api/cohorts?page=1&size=3", "Cohorts page=1 size=3")

    print("\n[done] Test complete")


if __name__ == "__main__":
    main()

