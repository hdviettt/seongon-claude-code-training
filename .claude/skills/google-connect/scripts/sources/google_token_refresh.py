#!/usr/bin/env python3
"""PostToolUse hook - auto-refresh Google OAuth token khi gap loi het han.

Canonical location after install: .claude/hooks/google_token_refresh.py
(installed by google-connect Step 5 via install.py)

Kich hoat khi:
  - tool_name == "Bash"
  - command hoac output co dau hieu Google API
  - output chua dau hieu token het han

Khi match, chay .claude/skills/lib/oauth_refresh.py (mo browser, doi user xac thuc, ghi
GOOGLE_REFRESH_TOKEN moi vao .env). Sau do bao Claude retry lenh truoc do qua exit code 2.
"""
import sys
import json
import subprocess
import os
from pathlib import Path

GOOGLE_API_HINTS = (
    "googleapis.com",
    "gsheets.py",
    "create_gdoc",
    "GOOGLE_REFRESH_TOKEN",
    "google-auth",
    "googleapiclient",
    "gspread",
    "oauth2.googleapis",
)

TOKEN_ERROR_PATTERNS = (
    "invalid_grant",
    "Token has been expired or revoked",
    "Request had invalid authentication credentials",
    "UNAUTHENTICATED",
    "invalid_rapt",
    "invalid_token",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REFRESH_SCRIPT = PROJECT_ROOT / ".claude" / "skills" / "lib" / "oauth_refresh.py"
LOCK_FILE = PROJECT_ROOT / ".claude" / "hooks" / ".oauth_refresh.lock"


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    cmd = payload.get("tool_input", {}).get("command", "") or ""
    resp = payload.get("tool_response", {}) or {}
    output = (
        str(resp.get("stdout", ""))
        + "\n"
        + str(resp.get("stderr", ""))
        + "\n"
        + str(resp.get("error", ""))
    )

    if not any(h in cmd or h in output for h in GOOGLE_API_HINTS):
        sys.exit(0)

    if not any(p in output for p in TOKEN_ERROR_PATTERNS):
        sys.exit(0)

    if not (resp.get("stderr") or resp.get("error") or resp.get("interrupted")):
        if "Traceback" not in output and "HTTPError" not in output:
            sys.exit(0)

    if LOCK_FILE.exists():
        try:
            age = abs(__import__("time").time() - LOCK_FILE.stat().st_mtime)
        except Exception:
            age = 0
        if age < 30:
            print(
                "[google-token-refresh] Vua refresh xong, bo qua loi nay (co the do cache token cu).",
                file=sys.stderr,
            )
            sys.exit(0)

    if not REFRESH_SCRIPT.exists():
        print(
            f"[google-token-refresh] Khong tim thay {REFRESH_SCRIPT}. Bo qua.",
            file=sys.stderr,
        )
        sys.exit(0)

    print(
        "[google-token-refresh] Phat hien Google OAuth token het han. "
        "Mo browser de xac thuc lai...",
        file=sys.stderr,
    )

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    try:
        result = subprocess.run(
            [sys.executable, str(REFRESH_SCRIPT)],
            timeout=600,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            cwd=str(PROJECT_ROOT),
        )
    except subprocess.TimeoutExpired:
        print(
            "[google-token-refresh] Het 10 phut cho user xac thuc. Vui long chay lai sau.",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOCK_FILE.write_text("ok", encoding="utf-8")
    except Exception:
        pass

    if result.returncode == 0:
        print(
            "[google-token-refresh] Da refresh GOOGLE_REFRESH_TOKEN. "
            "Hay chay lai lenh Bash truoc do (lenh vua loi).",
            file=sys.stderr,
        )
        sys.exit(2)
    else:
        tail = (result.stderr or result.stdout or "")[-500:]
        print(
            f"[google-token-refresh] Refresh that bai (exit {result.returncode}). "
            f"Output cuoi:\n{tail}",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
