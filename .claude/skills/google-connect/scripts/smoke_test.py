#!/usr/bin/env python3
"""smoke_test.py - verify Google OAuth connection works end-to-end.

Steps:
  1. Load .env from project root
  2. Refresh access token from GOOGLE_REFRESH_TOKEN
  3. Call Google Sheets API metadata endpoint on a known public sheet
  4. Print OK / FAIL with diagnostics

Exit codes:
  0 - smoke test PASS
  1 - .env missing or incomplete
  2 - refresh token call failed
  3 - API call failed
"""
import os
import sys
import json
import argparse
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

ENV_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / ".env"

# Public sample sheet maintained by Google as API test target.
# Anyone with read API access can hit this.
TEST_SHEET_ID = "1qpyC0XzvTcKT6EISywvqESX3A0MwQoFDE8p-Bll4hfg"


def log(msg):
    print(f"[smoke] {msg}", flush=True)


def fail(msg, code):
    print(f"[smoke] FAIL: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


def load_env():
    if not ENV_PATH.exists():
        fail(f".env khong ton tai tai {ENV_PATH}", 1)

    env = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip("\"'")

    required = ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"]
    missing = [k for k in required if not env.get(k)]
    if missing:
        fail(f".env thieu cac bien: {', '.join(missing)}", 1)
    return env


def refresh_access_token(env, verbose=False):
    body = urlencode({
        "client_id": env["GOOGLE_CLIENT_ID"],
        "client_secret": env["GOOGLE_CLIENT_SECRET"],
        "refresh_token": env["GOOGLE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    req = Request(
        "https://oauth2.googleapis.com/token",
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        resp = urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
        if "access_token" not in data:
            fail(f"Response thieu access_token: {data}", 2)
        if verbose:
            log(f"Refresh OK - access_token len: {len(data['access_token'])}")
            log(f"  Expires in: {data.get('expires_in', '?')}s")
            log(f"  Scopes: {data.get('scope', '?')}")
        return data["access_token"]
    except HTTPError as e:
        body = e.read().decode()
        fail(
            f"HTTP {e.code} refresh token. Response: {body}\n"
            f"Likely causes:\n"
            f"  - GOOGLE_REFRESH_TOKEN sai/expired -> re-run Step 4 OAuth flow\n"
            f"  - GOOGLE_CLIENT_ID/SECRET sai -> re-check .env",
            2,
        )
    except URLError as e:
        fail(f"Network error khi goi oauth2.googleapis.com: {e.reason}", 2)


def test_sheets_api(access_token, verbose=False):
    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/{TEST_SHEET_ID}"
        "?fields=properties.title"
    )
    req = Request(url, headers={"Authorization": f"Bearer {access_token}"})
    try:
        resp = urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
        title = data.get("properties", {}).get("title", "?")
        if verbose:
            log(f"API call OK - sheet title: '{title}'")
        return True
    except HTTPError as e:
        body = e.read().decode()[:500]
        causes = []
        if e.code == 401:
            causes.append("Token het hieu luc - tinh huong la 0 (vua refresh xong)")
            causes.append("Scope spreadsheets chua duoc grant -> Step 4 re-run + grant tat ca")
        elif e.code == 403:
            causes.append("Google Sheets API chua enable o Cloud Console")
            causes.append("Quota het - check Cloud Console quotas")
        elif e.code == 404:
            causes.append("Test sheet khong ton tai - chinh TEST_SHEET_ID trong script")
        fail(
            f"HTTP {e.code} call Sheets API.\nResponse: {body}\n"
            f"Likely causes:\n" + "\n".join(f"  - {c}" for c in causes),
            3,
        )
    except URLError as e:
        fail(f"Network error khi goi sheets.googleapis.com: {e.reason}", 3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    log(f".env path: {ENV_PATH}")
    env = load_env()
    log("Step 1/3: .env loaded - OK")

    if args.verbose:
        log(f"CLIENT_ID prefix: {env['GOOGLE_CLIENT_ID'][:20]}...")

    access_token = refresh_access_token(env, args.verbose)
    log("Step 2/3: Refresh access token - OK")

    test_sheets_api(access_token, args.verbose)
    log("Step 3/3: Sheets API call - OK")

    log("=" * 50)
    log("SMOKE TEST PASSED - Google API hoat dong dung.")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
