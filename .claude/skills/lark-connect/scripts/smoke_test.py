#!/usr/bin/env python3
"""smoke_test.py - verify lark-mcp server respond JSON-RPC tools/list.

Spawn lark_mcp_runner.py, send tools/list request, parse response.

Exit codes:
  0 - PASS, >=1 tool returned
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
LARK_MCP_CACHE = Path.home() / ".lark-mcp"


def log(msg):
    print(f"[smoke] {msg}", flush=True)


def fail(msg, code):
    print(f"[smoke] FAIL: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


def check_env():
    if not ENV_PATH.exists():
        fail(f".env khong ton tai tai {ENV_PATH}", 1)
    content = ENV_PATH.read_text(encoding="utf-8")
    if "LARK_APP_ID=" not in content or "LARK_APP_SECRET=" not in content:
        fail(".env thieu LARK_APP_ID hoac LARK_APP_SECRET", 1)
    log(".env OK")


def check_token_cache(verbose=False):
    """Verify lark-mcp login da chay."""
    if not LARK_MCP_CACHE.exists():
        log(f"WARN: {LARK_MCP_CACHE} khong ton tai")
        log("Co the lark-mcp chua login. Chay:")
        log("  npx -y @larksuiteoapi/lark-mcp login -a <APP_ID> -s <APP_SECRET>")
        # Khong fail - lark-mcp moi version co the cache cho khac
    else:
        if verbose:
            files = list(LARK_MCP_CACHE.glob("*"))
            log(f"{LARK_MCP_CACHE} co {len(files)} files")


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
            timeout=60,
            env=env,
        )
    except subprocess.TimeoutExpired:
        fail("lark-mcp spawn timeout 60s - co the npx dang download package", 2)
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

    # Parse stdout cho JSON-RPC response
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
            f"  - lark-mcp chua login -> chay step 5\n"
            f"  - Scopes chua approve trong Lark Console\n"
            f"  - App chua Release -> Lark Console -> Version Management",
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
    log("Step 1/3: .env validated - OK")

    check_token_cache(args.verbose)
    log("Step 2/3: Token cache check - OK")

    tools = test_tools_list(args.verbose)
    log("Step 3/3: tools/list - OK")

    log("=" * 50)
    log(f"SMOKE TEST PASSED - lark-mcp ready ({len(tools)} tools)")
    log("Restart Claude Code de Claude load MCP. Sau do thu:")
    log('  "Gui Lark cho group X: Test from Claude"')


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
