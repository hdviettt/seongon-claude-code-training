#!/usr/bin/env python3
"""smoke_test.py - verify lark-mcp tenant mode responds JSON-RPC tools/list.

Spawn lark_mcp_runner.py, send tools/list request, parse response, verify >=10 tools.

Tenant mode khong can token cache (lark-mcp tu lay tenant_access_token tu APP_ID + SECRET).

Exit codes:
  0 - PASS, >=10 tools returned
  1 - .env / config issue
  2 - lark-mcp spawn fail
  3 - tools/list empty hoac fail
"""
import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
RUNNER = SKILL_DIR / "scripts" / "lark_mcp_runner.py"
ENV_PATH = SKILL_DIR.parent.parent.parent / ".env"


def log(msg):
    print(f"[smoke] {msg}", flush=True)


def fail(msg, code):
    print(f"[smoke] FAIL: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


def check_env():
    if not ENV_PATH.exists():
        fail(f".env khong ton tai tai {ENV_PATH}", 1)
    content = ENV_PATH.read_text(encoding="utf-8")
    required = ["LARK_APP_ID=", "LARK_APP_SECRET=", "LARK_DOMAIN="]
    missing = [k.rstrip("=") for k in required if k not in content]
    if missing:
        fail(f".env thieu cac bien: {', '.join(missing)}", 1)
    log(".env OK")


def test_tools_list(verbose=False):
    """Spawn lark-mcp runner, send JSON-RPC tools/list."""
    if not RUNNER.exists():
        fail(f"Runner script khong ton tai: {RUNNER}", 1)

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {},
    }
    request_str = json.dumps(request) + "\n"

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    try:
        proc = subprocess.run(
            [sys.executable, str(RUNNER)],
            input=request_str,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
            env=env,
        )
    except subprocess.TimeoutExpired:
        fail(
            "lark-mcp spawn timeout 90s - co the npx dang download package lan dau (~50MB). "
            "Retry sau 1 phut.",
            2,
        )
    except FileNotFoundError:
        fail(f"Python khong tim thay {sys.executable}", 2)

    if verbose:
        log(f"Runner exit code: {proc.returncode}")
        log(f"Runner stderr (last 500 chars):\n{proc.stderr[-500:]}")

    if proc.returncode != 0:
        fail(
            f"Runner exit {proc.returncode}. Stderr:\n{proc.stderr[-1000:]}",
            2,
        )

    tools = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            resp = json.loads(line)
            if resp.get("id") == 1 and "result" in resp:
                tools = resp["result"].get("tools", [])
                break
        except json.JSONDecodeError:
            continue

    if not tools:
        fail(
            "tools/list response empty hoac khong parse duoc.\n"
            f"Stdout sample:\n{proc.stdout[:500]}\n"
            f"Likely causes:\n"
            f"  - App chua Released o Lark Console -> Version Management -> Submit + Self-approve\n"
            f"  - Scopes chua approve -> Lark Console -> Permissions & Scopes\n"
            f"  - LARK_APP_ID/SECRET sai -> re-check .env",
            3,
        )

    if verbose:
        sample = [t.get("name") for t in tools[:5]]
        log(f"Sample tools: {sample}")

    log(f"PASS - lark-mcp responded with {len(tools)} tools")
    return tools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    log(f"Project root: {SKILL_DIR.parent.parent.parent}")

    check_env()
    log("Step 1/2: .env validated - OK")

    tools = test_tools_list(args.verbose)
    log("Step 2/2: tools/list - OK")

    log("=" * 50)
    log(f"SMOKE TEST PASSED - lark-mcp tenant mode ready ({len(tools)} tools)")
    log("RESTART Claude Code (quit process, mo lai) de Claude load MCP.")
    log("Sau do trong CC:")
    log('  "List cac nhom chat Lark bot dang o"')
    log('  "Send message qua Lark cho group X: Test"')


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
