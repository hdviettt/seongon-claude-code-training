#!/usr/bin/env python3
"""smoke_test.py - verify Together AI key + generate 1 test image."""
import sys
import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
GENERATE = SKILL_DIR / "scripts" / "generate.py"


def main():
    if not GENERATE.exists():
        print(f"[smoke] FAIL: {GENERATE} not found", file=sys.stderr)
        sys.exit(1)

    print("[smoke] Calling generate.py with test prompt...", flush=True)
    result = subprocess.run(
        [
            sys.executable, str(GENERATE),
            "--prompt", "A minimalist test logo design, dark navy background, modern sans-serif typography",
            "--model", "black-forest-labs/FLUX.1-schnell",
            "--width", "1024", "--height", "1024",
            "--n", "1",
        ],
        capture_output=True, text=True, timeout=90,
    )
    print(f"[smoke] Exit code: {result.returncode}", flush=True)
    if result.stderr:
        print(f"[smoke] Stderr:\n{result.stderr[-1000:]}", flush=True)
    if result.returncode == 0:
        print(f"[smoke] PASS")
        print(f"[smoke] Stdout: {result.stdout[-500:]}")
        sys.exit(0)
    else:
        print(f"[smoke] FAIL", file=sys.stderr)
        sys.exit(result.returncode)


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
