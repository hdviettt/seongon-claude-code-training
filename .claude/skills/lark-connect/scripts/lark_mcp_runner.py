#!/usr/bin/env python3
"""lark_mcp_runner.py - wrapper spawn lark-mcp server với credentials từ .env.

Pattern tach bach credentials (secret, in .env) khoi MCP config (.mcp.json, can commit len git).

Runtime: Claude Code spawn script nay theo .mcp.json entry. Script doc .env, spawn
`npx -y @larksuiteoapi/lark-mcp mcp --domain ... --token-mode tenant_access_token ...`
voi credentials tu .env. Stdio passed through Claude Code <-> lark-mcp.

Skill nay CHI support tenant_access_token (bot mode). user_access_token (OAuth flow)
hien co bug voi Larksuite (error 20029 du redirect URL whitelist dung).
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"


def load_env():
    if not ENV_PATH.exists():
        print(
            f"[lark-mcp-runner] Khong tim thay .env tai {ENV_PATH}",
            file=sys.stderr,
        )
        print(
            "[lark-mcp-runner] Chay `/lark-connect` de setup truoc.",
            file=sys.stderr,
        )
        sys.exit(1)

    env = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip("\"'")
    return env


def main():
    env_vars = load_env()

    app_id = env_vars.get("LARK_APP_ID")
    app_secret = env_vars.get("LARK_APP_SECRET")
    domain = env_vars.get("LARK_DOMAIN", "https://open.larksuite.com")
    tools = env_vars.get("LARK_TOOLS", "")

    if not app_id or not app_secret:
        print(
            "[lark-mcp-runner] .env thieu LARK_APP_ID hoac LARK_APP_SECRET",
            file=sys.stderr,
        )
        sys.exit(1)

    # Skill chi support tenant_access_token. user_access_token co bug voi Larksuite.
    args = [
        "npx", "-y", "@larksuiteoapi/lark-mcp",
        "mcp",
        "-a", app_id,
        "-s", app_secret,
        "--domain", domain,
        "--token-mode", "tenant_access_token",
    ]

    if tools:
        args.extend(["-t", tools])

    # Pass through stdio - Claude Code <-> lark-mcp
    try:
        os.execvp("npx", args)
    except FileNotFoundError:
        print(
            "[lark-mcp-runner] `npx` khong tim thay. Cai Node.js 18+ tu nodejs.org",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
