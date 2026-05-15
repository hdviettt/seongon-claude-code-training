#!/usr/bin/env python3
"""One-off Google OAuth refresh — opens browser, catches callback, updates .env.

Canonical location after install: .claude/skills/lib/oauth_refresh.py
(installed by google-connect Step 5 via install.py)

ENV_PATH resolves to project root: __file__ -> .claude/skills/lib/oauth_refresh.py
parent.parent.parent.parent -> project root -> .env
"""
import os, sys, json, secrets, webbrowser, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent.parent.parent / ".env"
SCOPES = " ".join([
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
])
PORT = 8080


def load_env():
    if not ENV_PATH.exists():
        print(f"Khong tim thay .env tai {ENV_PATH}", file=sys.stderr)
        print("Hay tao .env voi GOOGLE_CLIENT_ID va GOOGLE_CLIENT_SECRET truoc.", file=sys.stderr)
        sys.exit(1)
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip("\"'"))


def update_env_token(new_token):
    lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
    out, replaced = [], False
    for line in lines:
        if line.startswith("GOOGLE_REFRESH_TOKEN="):
            out.append(f"GOOGLE_REFRESH_TOKEN={new_token}")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(f"GOOGLE_REFRESH_TOKEN={new_token}")
    ENV_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")


state = secrets.token_urlsafe(16)
result = {}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a, **kw):
        pass

    def do_GET(self):
        q = urllib.parse.urlparse(self.path).query
        params = dict(urllib.parse.parse_qsl(q))
        result.update(params)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        msg = (
            "OK - ban quay lai terminal."
            if "code" in params
            else f"Loi: {params}"
        )
        self.wfile.write(
            f"<html><body><h2>{msg}</h2></body></html>".encode("utf-8")
        )


def main():
    load_env()
    cid = os.environ.get("GOOGLE_CLIENT_ID")
    csec = os.environ.get("GOOGLE_CLIENT_SECRET")
    if not cid or not csec:
        print("Thieu GOOGLE_CLIENT_ID hoac GOOGLE_CLIENT_SECRET trong .env", file=sys.stderr)
        sys.exit(1)

    server = HTTPServer(("127.0.0.1", PORT), Handler)
    redirect = f"http://localhost:{PORT}"

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid,
        "redirect_uri": redirect,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    })

    print(f"Mo URL nay neu browser khong tu mo:\n{auth_url}\n", flush=True)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    print(f"Dang cho callback tren {redirect} ...", flush=True)
    while "code" not in result and "error" not in result:
        server.handle_request()

    if "error" in result:
        print(f"OAuth error: {result}", file=sys.stderr)
        sys.exit(1)
    if result.get("state") != state:
        print("State mismatch", file=sys.stderr)
        sys.exit(1)

    body = urllib.parse.urlencode({
        "client_id": cid,
        "client_secret": csec,
        "code": result["code"],
        "redirect_uri": redirect,
        "grant_type": "authorization_code",
    }).encode()
    req = Request(
        "https://oauth2.googleapis.com/token",
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    tok = json.loads(urlopen(req, timeout=30).read().decode())
    if "refresh_token" not in tok:
        print(f"Khong nhan duoc refresh_token: {tok}", file=sys.stderr)
        print(
            "Co the do app da duoc authorize truoc. "
            "Vao https://myaccount.google.com/permissions remove app roi chay lai.",
            file=sys.stderr,
        )
        sys.exit(1)

    update_env_token(tok["refresh_token"])
    print("OK - da cap nhat GOOGLE_REFRESH_TOKEN trong .env")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
