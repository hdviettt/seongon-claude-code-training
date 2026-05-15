#!/usr/bin/env python3
"""smoke_test.py - verify Together AI key + endpoint reachable.

--dry-run: chỉ check key + list models (free, không gen)
Full test: gen 1 video với kling-standard ($0.40)
"""
import sys
import subprocess
import argparse
import urllib.request
import json
from pathlib import Path
from urllib.error import HTTPError

SKILL_DIR = Path(__file__).resolve().parent.parent
GENERATE = SKILL_DIR / "scripts" / "generate.py"


def load_api_key():
    cwd = Path.cwd()
    for p in [cwd] + list(cwd.parents):
        for fname in [".env", ".env.local"]:
            path = p / fname
            if not path.exists():
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("TOGETHER_AI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("\"'")
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Skip actual gen (chi check key + list video models)")
    args = parser.parse_args()

    key = load_api_key()
    if not key:
        print("[smoke] FAIL: TOGETHER_AI_API_KEY khong tim thay", file=sys.stderr)
        sys.exit(1)
    print(f"[smoke] API key loaded ({len(key)} chars)", flush=True)

    if args.dry_run:
        url = "https://api.together.xyz/v1/models"
        try:
            req = urllib.request.Request(url, headers={
                "Authorization": f"Bearer {key}",
                "User-Agent": "Mozilla/5.0 ClaudeCode-skill",
            })
            data = json.loads(urllib.request.urlopen(req, timeout=30).read())
            video_models = [m["id"] for m in data if m.get("type") == "video"]
            print(f"[smoke] Auth OK. Video models: {len(video_models)}", flush=True)
            for m in video_models[:8]:
                print(f"  - {m}", flush=True)
            if len(video_models) > 8:
                print(f"  ... và {len(video_models) - 8} models khác", flush=True)
            print("[smoke] PASS (dry-run: KHÔNG gen video)")
            sys.exit(0)
        except HTTPError as e:
            print(f"[smoke] FAIL: HTTP {e.code} listing models: {e.read().decode()[:200]}", file=sys.stderr)
            sys.exit(1)

    print("[smoke] WARN: Full test sẽ tốn ~$0.40 (kling-standard). Ctrl+C trong 5s để cancel.", flush=True)
    import time
    time.sleep(5)

    result = subprocess.run(
        [
            sys.executable, str(GENERATE),
            "--prompt", "A short cinematic clip: golden hour over a calm tropical beach, gentle waves",
            "--model", "kwaivgI/kling-2.1-standard",
            "--aspect", "16:9",
        ],
        capture_output=True, text=True, timeout=720,
    )
    print(f"[smoke] Exit: {result.returncode}", flush=True)
    if result.stderr:
        print(f"[smoke] Stderr (last 800):\n{result.stderr[-800:]}", flush=True)
    if result.returncode == 0:
        print(f"[smoke] PASS\n{result.stdout[-500:]}")
        sys.exit(0)
    else:
        sys.exit(result.returncode)


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
