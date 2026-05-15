#!/usr/bin/env python3
"""install.py - setup .env + .mcp.json + .gitignore cho lark-connect.

Chay tu skill Step 4. Operations (idempotent):
  1. Validate .env co LARK_APP_ID + LARK_APP_SECRET
  2. Write/patch .mcp.json voi entry "lark-mcp" tro toi lark_mcp_runner.py
  3. Ensure .gitignore co .env

Exit codes:
  0 - all OK
  1 - critical error (.env invalid, .mcp.json parse fail)
  2 - partial (gitignore fail, non-critical)
"""
import sys
import json
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SKILL_DIR.parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
MCP_CONFIG = PROJECT_ROOT / ".mcp.json"
GITIGNORE = PROJECT_ROOT / ".gitignore"

RUNNER_REL_PATH = ".claude/skills/lark-connect/scripts/lark_mcp_runner.py"


def log(msg):
    print(f"[install] {msg}", flush=True)


def err(msg):
    print(f"[install] ERROR: {msg}", file=sys.stderr, flush=True)


def warn(msg):
    print(f"[install] WARN: {msg}", file=sys.stderr, flush=True)


def validate_env():
    """Verify .env exists with LARK_APP_ID + LARK_APP_SECRET format-valid."""
    if not ENV_PATH.exists():
        err(f".env khong ton tai tai {ENV_PATH}")
        return False

    env = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip("\"'")

    app_id = env.get("LARK_APP_ID", "")
    app_secret = env.get("LARK_APP_SECRET", "")

    if not re.match(r"^cli_[a-zA-Z0-9]{12,20}$", app_id):
        err(f"LARK_APP_ID format invalid: '{app_id[:30]}'")
        err("  Expected: cli_<alphanumeric>, vd cli_a1b2c3d4e5f6g7h8")
        return False

    if len(app_secret) < 30:
        err(f"LARK_APP_SECRET too short ({len(app_secret)} chars, need 30+)")
        return False

    domain = env.get("LARK_DOMAIN", "https://open.larksuite.com")
    log(f".env validated: LARK_APP_ID={app_id[:15]}..., domain={domain}")
    return True


def patch_mcp_config():
    """Write/patch .mcp.json with lark-mcp server entry."""
    if MCP_CONFIG.exists():
        try:
            config = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f".mcp.json parse error: {e}")
            return False
    else:
        config = {}

    servers = config.setdefault("mcpServers", {})

    new_entry = {
        "command": "python",
        "args": [RUNNER_REL_PATH],
    }

    if "lark-mcp" in servers:
        existing = servers["lark-mcp"]
        if existing == new_entry:
            log(".mcp.json entry 'lark-mcp' da dung - skip")
        else:
            warn(".mcp.json entry 'lark-mcp' co conflict - overwriting")
            servers["lark-mcp"] = new_entry
    else:
        servers["lark-mcp"] = new_entry
        log("Added new 'lark-mcp' entry to .mcp.json")

    MCP_CONFIG.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    log(f"Updated {MCP_CONFIG}")
    return True


def ensure_gitignore():
    """Ensure .env in .gitignore if git repo."""
    if not (PROJECT_ROOT / ".git").exists():
        log("Khong phai git repo - skip .gitignore")
        return True

    if GITIGNORE.exists():
        content = GITIGNORE.read_text(encoding="utf-8")
        lines = [l.strip() for l in content.splitlines()]
        if ".env" in lines or ".env*" in lines or "*.env" in lines:
            log(".gitignore da co .env")
            return True
        new = content.rstrip() + "\n\n# Environment variables\n.env\n"
        GITIGNORE.write_text(new, encoding="utf-8")
        log("Appended .env to .gitignore")
    else:
        GITIGNORE.write_text("# Environment variables\n.env\n", encoding="utf-8")
        log("Created .gitignore with .env")
    return True


def main():
    log(f"Project root: {PROJECT_ROOT}")

    if not validate_env():
        sys.exit(1)

    if not patch_mcp_config():
        sys.exit(1)

    if not ensure_gitignore():
        warn("gitignore update fail (non-critical)")

    log("=" * 50)
    log("Install hoan tat.")
    log("Next step: chay `npx -y @larksuiteoapi/lark-mcp login -a $LARK_APP_ID -s $LARK_APP_SECRET`")
    log("Sau khi login xong, RESTART Claude Code de load MCP.")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
