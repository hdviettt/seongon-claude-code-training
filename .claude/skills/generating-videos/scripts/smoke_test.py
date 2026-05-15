#!/usr/bin/env python3
"""smoke_test.py - verify GEMINI_API_KEY + submit 1 short test video.

Note: VEO 3 = paid model. Smoke test will incur cost ~$0.40 (720p/8s).
Để skip actual generation, dùng --dry-run (chỉ check API key + endpoint reachable).
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
API_BASE = "https://generativelanguage.googleapis.com/v1beta"


def load_api_key():
    cwd = Path.cwd()
    for p in [cwd] + list(cwd.parents):
        for fname in [".env", ".env.local"]:
            path = p / fname
            if not path.exists():
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("\"'")
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Skip actual gen (chi check API key)")
    args = parser.parse_args()

    key = load_api_key()
    if not key:
        print("[smoke] FAIL: GEMINI_API_KEY khong tim thay trong .env/.env.local", file=sys.stderr)
        sys.exit(1)
    print(f"[smoke] API key loaded ({len(key)} chars, prefix '{key[:6]}...')", flush=True)

    if args.dry_run:
        # Just list models to verify auth
        url = f"{API_BASE}/models?key={key}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 ClaudeCode-skill"})
            data = json.loads(urllib.request.urlopen(req, timeout=30).read())
            veo_models = [m["name"] for m in data.get("models", []) if "veo" in m.get("name", "").lower()]
            print(f"[smoke] Auth OK. VEO models available: {len(veo_models)}", flush=True)
            for m in veo_models[:5]:
                print(f"  - {m}", flush=True)
            print("[smoke] PASS (dry-run: KHÔNG gen video thật)")
            sys.exit(0)
        except HTTPError as e:
            print(f"[smoke] FAIL: HTTP {e.code} listing models: {e.read().decode()[:200]}", file=sys.stderr)
            sys.exit(1)

    # Full test - sẽ tốn ~$0.40
    print("[smoke] WARN: Full test sẽ tốn ~$0.40 (VEO 3 paid). Ctrl+C trong 5s để cancel.", flush=True)
    import time
    time.sleep(5)

    result = subprocess.run(
        [
            sys.executable, str(GENERATE),
            "--prompt", "A short cinematic clip: golden hour over a calm lake, gentle ripples, no people",
            "--model", "veo-3.1-fast-generate-preview",
            "--resolution", "720p",
            "--duration", "4",
            "--aspect", "16:9",
        ],
        capture_output=True, text=True, timeout=420,
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
