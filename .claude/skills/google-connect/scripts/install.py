#!/usr/bin/env python3
"""install.py - deploy oauth_refresh.py + hook + patch settings.local.json.

Chay tu project root. Skill google-connect Step 5 invoke script nay.

Operations (idempotent - chay nhieu lan an toan):
  1. Copy sources/oauth_refresh.py -> .claude/skills/lib/oauth_refresh.py
  2. Copy sources/google_token_refresh.py -> .claude/hooks/google_token_refresh.py
  3. Patch .claude/settings.local.json:
     - Add PostToolUse hook entry (merge, khong overwrite)
  4. Ensure .gitignore has .env

Exit codes:
  0 - all OK
  1 - critical error (missing source files)
  2 - partial success (some steps fail, see stderr)
"""
import sys
import json
import shutil
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent  # .claude/skills/google-connect/
PROJECT_ROOT = SKILL_DIR.parent.parent.parent  # project root
SOURCES = SKILL_DIR / "scripts" / "sources"

LIB_DEST = PROJECT_ROOT / ".claude" / "skills" / "lib" / "oauth_refresh.py"
HOOK_DEST = PROJECT_ROOT / ".claude" / "hooks" / "google_token_refresh.py"
SETTINGS_PATH = PROJECT_ROOT / ".claude" / "settings.local.json"
GITIGNORE_PATH = PROJECT_ROOT / ".gitignore"

HOOK_ENTRY = {
    "type": "command",
    "command": "python .claude/hooks/google_token_refresh.py",
}


def log(msg):
    print(f"[install] {msg}", flush=True)


def warn(msg):
    print(f"[install] WARN: {msg}", file=sys.stderr, flush=True)


def err(msg):
    print(f"[install] ERROR: {msg}", file=sys.stderr, flush=True)


def copy_file(src, dest):
    """Copy file, create parent dirs if needed."""
    if not src.exists():
        err(f"Source khong ton tai: {src}")
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    log(f"Copied {src.name} -> {dest}")
    return True


def patch_settings():
    """Merge PostToolUse hook entry into settings.local.json."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)

    if SETTINGS_PATH.exists():
        try:
            settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"settings.local.json hong: {e}")
            return False
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})
    post_tool_use = hooks.setdefault("PostToolUse", [])

    # Find existing Bash matcher entry
    bash_matcher = None
    for entry in post_tool_use:
        if entry.get("matcher") == "Bash":
            bash_matcher = entry
            break

    if bash_matcher is None:
        post_tool_use.append({
            "matcher": "Bash",
            "hooks": [HOOK_ENTRY],
        })
        log("Added new PostToolUse Bash matcher")
    else:
        existing_hooks = bash_matcher.setdefault("hooks", [])
        # Check if hook already exists
        already = any(
            h.get("command") == HOOK_ENTRY["command"] for h in existing_hooks
        )
        if already:
            log("Hook entry da ton tai - skip")
        else:
            existing_hooks.append(HOOK_ENTRY)
            log("Appended hook entry to existing Bash matcher")

    SETTINGS_PATH.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    log(f"Updated {SETTINGS_PATH}")
    return True


def ensure_gitignore():
    """Ensure .env is in .gitignore."""
    if not (PROJECT_ROOT / ".git").exists():
        log("Khong phai git repo - skip .gitignore check")
        return True

    if GITIGNORE_PATH.exists():
        content = GITIGNORE_PATH.read_text(encoding="utf-8")
        lines = [l.strip() for l in content.splitlines()]
        if ".env" in lines or ".env*" in lines or "*.env" in lines:
            log(".gitignore da co .env entry")
            return True
        # Append
        new_content = content.rstrip() + "\n\n# Environment variables\n.env\n"
        GITIGNORE_PATH.write_text(new_content, encoding="utf-8")
        log("Appended .env to .gitignore")
    else:
        GITIGNORE_PATH.write_text("# Environment variables\n.env\n", encoding="utf-8")
        log("Created .gitignore with .env entry")
    return True


def main():
    log(f"Project root: {PROJECT_ROOT}")
    log(f"Skill dir: {SKILL_DIR}")

    src_oauth = SOURCES / "oauth_refresh.py"
    src_hook = SOURCES / "google_token_refresh.py"

    if not src_oauth.exists() or not src_hook.exists():
        err(f"Thieu source files trong {SOURCES}")
        err(f"  oauth_refresh.py exists: {src_oauth.exists()}")
        err(f"  google_token_refresh.py exists: {src_hook.exists()}")
        sys.exit(1)

    fails = []

    if not copy_file(src_oauth, LIB_DEST):
        fails.append("copy oauth_refresh")

    if not copy_file(src_hook, HOOK_DEST):
        fails.append("copy hook")

    if not patch_settings():
        fails.append("patch settings")

    if not ensure_gitignore():
        warn("ensure_gitignore failed (non-critical)")

    if fails:
        err(f"Cac buoc fail: {', '.join(fails)}")
        sys.exit(2)

    log("=" * 50)
    log("Install hoan tat. Files deployed:")
    log(f"  - {LIB_DEST}")
    log(f"  - {HOOK_DEST}")
    log(f"  - {SETTINGS_PATH} (PostToolUse hook registered)")
    log("Hook se tu kich hoat khi Bash command gap loi Google OAuth.")


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
