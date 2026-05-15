#!/usr/bin/env python3
"""generate.py - call Together AI FLUX, download image, save local.

Usage:
  python generate.py --prompt "..." [--model X] [--width N --height N] [--n N] [--output-dir D]

Reads TOGETHER_AI_API_KEY tu .env (priority) hoac .env.local (fallback).
Output: <output-dir>/<slug>-NNN.jpg + <slug>-NNN.json metadata
Exit 0 = success, 1 = config error, 2 = API error, 3 = save error.
"""
import os
import sys
import json
import argparse
import re
import datetime
import urllib.request
from pathlib import Path
from urllib.error import HTTPError

UA = "Mozilla/5.0 (compatible; ClaudeCode-generating-images/1.0)"
API_URL = "https://api.together.xyz/v1/images/generations"


def find_project_root():
    """Walk up tu cwd tim project root (chua .env, .env.local, .git, hoac .claude)."""
    cwd = Path.cwd()
    for p in [cwd] + list(cwd.parents):
        if (p / ".env").exists() or (p / ".env.local").exists() or (p / ".git").exists() or (p / ".claude").exists():
            return p
    return cwd


def load_api_key():
    """Doc TOGETHER_AI_API_KEY tu .env (uu tien) hoac .env.local."""
    root = find_project_root()
    for fname in [".env", ".env.local"]:
        path = root / fname
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("TOGETHER_AI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip("\"'")
                return key, path
    print(f"[generate] ERROR: TOGETHER_AI_API_KEY khong tim thay trong .env hoac .env.local tai {root}", file=sys.stderr)
    print(f"[generate] Apply free key tai https://api.together.ai/settings/api-keys", file=sys.stderr)
    sys.exit(1)


def slugify(s, maxlen=50):
    """Convert prompt to ASCII kebab-case slug."""
    # Strip Vietnamese diacritics rough
    vn = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
    en = "aaaaaaaaaaaaaaaaaeeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd"
    s = s.lower()
    s = "".join(en[vn.index(c)] if c in vn else c for c in s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:maxlen]


def generate(api_key, prompt, model, width, height, steps, n):
    """POST to Together AI, return list of image URLs."""
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "n": n,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": UA,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read())
        return [img["url"] for img in data.get("data", [])]
    except HTTPError as e:
        body_text = e.read().decode()
        print(f"[generate] API error HTTP {e.code}: {body_text[:500]}", file=sys.stderr)
        sys.exit(2)


def download_image(url, dest_path):
    """Download URL, save to dest_path. Return size in bytes."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(data)
        return len(data)
    except Exception as e:
        print(f"[generate] Download error: {e}", file=sys.stderr)
        sys.exit(3)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--model", default="black-forest-labs/FLUX.1-kontext-max")
    p.add_argument("--width", type=int, default=1024)
    p.add_argument("--height", type=int, default=1024)
    p.add_argument("--steps", type=int, default=None, help="Default: 4 cho schnell, 28 cho dev/pro/max")
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--output-dir", default="output/images")
    args = p.parse_args()

    if len(args.prompt) < 10:
        print("[generate] ERROR: Prompt qua ngan (<10 chars). Cung cap mo ta chi tiet hon.", file=sys.stderr)
        sys.exit(1)
    if args.width > 1792 or args.height > 1792:
        print("[generate] ERROR: Dimensions vuot 1792 (FLUX API hard limit cho schnell/dev/pro).", file=sys.stderr)
        sys.exit(1)
    if args.width < 64 or args.height < 64:
        print("[generate] ERROR: Dimensions duoi 64.", file=sys.stderr)
        sys.exit(1)
    if args.n > 4:
        print("[generate] ERROR: n > 4 (API limit). Chay nhieu request neu can.", file=sys.stderr)
        sys.exit(1)

    # Default steps tuy model
    if args.steps is None:
        args.steps = 4 if "schnell" in args.model else 28

    api_key, env_path = load_api_key()
    print(f"[generate] API key loaded tu {env_path.name}", file=sys.stderr)
    print(f"[generate] Calling {args.model} ({args.width}x{args.height}, steps={args.steps}, n={args.n})...", file=sys.stderr)

    urls = generate(api_key, args.prompt, args.model, args.width, args.height, args.steps, args.n)
    if not urls:
        print("[generate] ERROR: No URLs returned", file=sys.stderr)
        sys.exit(2)

    root = find_project_root()
    out_dir = root / args.output_dir
    slug = slugify(args.prompt)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base_slug = f"{slug}-{timestamp}"

    results = []
    for i, url in enumerate(urls, 1):
        suffix = f"-{i:03d}" if len(urls) > 1 else ""
        img_path = out_dir / f"{base_slug}{suffix}.jpg"

        size = download_image(url, img_path)
        results.append({"path": str(img_path), "size": size})
        print(f"[generate] OK: {img_path} ({size}B)", file=sys.stderr)

    # JSON output cho parent process (chỉ stdout, không ghi file)
    print(json.dumps({"images": results, "out_dir": str(out_dir), "model": args.model, "prompt": args.prompt}, ensure_ascii=False))


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
