#!/usr/bin/env python3
"""Wrapper - delegate to sources/oauth_refresh.py.

Step 4 cua skill goi script nay (chu khong goi truc tiep sources/).
Source file la canonical version se duoc install ra .claude/skills/lib/.
"""
import sys
import subprocess
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "sources" / "oauth_refresh.py"

if not SOURCE.exists():
    print(f"Khong tim thay {SOURCE}", file=sys.stderr)
    sys.exit(1)

result = subprocess.run(
    [sys.executable, str(SOURCE)],
    cwd=str(SOURCE.parent.parent.parent.parent.parent),  # project root
)
sys.exit(result.returncode)
