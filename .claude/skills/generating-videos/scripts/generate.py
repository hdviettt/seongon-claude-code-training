#!/usr/bin/env python3
"""generate.py - submit Together AI video generation, poll, download MP4.

Usage:
  python generate.py --prompt "..." [--model X] [--aspect 16:9]

Reads TOGETHER_AI_API_KEY tu .env (priority) hoac .env.local (fallback).
Output: <output-dir>/<slug>-<timestamp>.mp4 + .json metadata
Exit: 0=success, 1=config, 2=API, 3=save, 4=timeout
"""
import os
import sys
import json
import time
import argparse
import re
import datetime
import urllib.request
from pathlib import Path
from urllib.error import HTTPError

UA = "Mozilla/5.0 (compatible; ClaudeCode-generating-videos/1.0)"
API_BASE = "https://api.together.xyz/v2/videos"
POLL_INTERVAL = 15
MAX_WAIT = 600  # 10 minutes


def find_project_root():
    cwd = Path.cwd()
    for p in [cwd] + list(cwd.parents):
        if (p / ".env").exists() or (p / ".env.local").exists() or (p / ".git").exists() or (p / ".claude").exists():
            return p
    return cwd


def load_api_key():
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
    print(f"[generate] ERROR: TOGETHER_AI_API_KEY khong tim thay tai {root}/.env hoac .env.local", file=sys.stderr)
    print(f"[generate] Apply tai https://api.together.ai/settings/api-keys", file=sys.stderr)
    sys.exit(1)


def slugify(s, maxlen=50):
    vn = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
    en = "aaaaaaaaaaaaaaaaaeeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd"
    s = s.lower()
    s = "".join(en[vn.index(c)] if c in vn else c for c in s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:maxlen]


def submit_job(api_key, prompt, model, aspect):
    """POST /v2/videos, return job_id."""
    # Map aspect to explicit width/height (veo-3.0 yêu cầu width+height tách rời, không phải `size`)
    if aspect == "9:16":
        w, h = 1080, 1920
    else:  # 16:9 default
        w, h = 1920, 1080

    body_dict = {
        "model": model,
        "prompt": prompt,
        "width": w,
        "height": h,
    }

    body = json.dumps(body_dict).encode("utf-8")
    req = urllib.request.Request(
        API_BASE,
        data=body, method="POST",
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
        if "id" not in data:
            print(f"[generate] ERROR: No job id. Response: {data}", file=sys.stderr)
            sys.exit(2)
        return data
    except HTTPError as e:
        print(f"[generate] Submit HTTP {e.code}: {e.read().decode()[:500]}", file=sys.stderr)
        sys.exit(2)


def poll_job(api_key, job_id):
    """GET /v2/videos/{id} until completed."""
    url = f"{API_BASE}/{job_id}"
    start = time.time()
    last_log = start
    headers = {"Authorization": f"Bearer {api_key}", "User-Agent": UA}

    while True:
        elapsed = int(time.time() - start)
        if elapsed > MAX_WAIT:
            print(f"[generate] TIMEOUT {MAX_WAIT}s waiting completion", file=sys.stderr)
            sys.exit(4)

        try:
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req, timeout=30)
            data = json.loads(resp.read())
        except HTTPError as e:
            print(f"[generate] Poll HTTP {e.code}, retrying...", file=sys.stderr)
            time.sleep(POLL_INTERVAL)
            continue

        status = data.get("status", "?")
        if status in ("completed", "succeeded", "done", "ready"):
            return data
        if status in ("failed", "error", "cancelled"):
            print(f"[generate] Job FAILED: {data}", file=sys.stderr)
            sys.exit(2)

        if time.time() - last_log >= 30:
            print(f"[generate] Polling... {elapsed}s elapsed (status: {status})", file=sys.stderr)
            last_log = time.time()

        time.sleep(POLL_INTERVAL)


def download_video(url, dest_path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
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
    p.add_argument("--model", default="google/veo-3.0",
                   help="google/veo-3.0 (default), google/veo-3.0-fast, google/veo-3.0-audio, openai/sora-2, kwaivgI/kling-2.1-standard, etc.")
    p.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"])
    p.add_argument("--output-dir", default="output/videos")
    args = p.parse_args()

    if len(args.prompt) < 15:
        print("[generate] ERROR: Prompt qua ngan (<15 chars).", file=sys.stderr)
        sys.exit(1)

    api_key, env_path = load_api_key()
    print(f"[generate] API key loaded tu {env_path.name}", file=sys.stderr)
    print(f"[generate] Submitting {args.model} (aspect {args.aspect})...", file=sys.stderr)

    job = submit_job(api_key, args.prompt, args.model, args.aspect)
    job_id = job["id"]
    print(f"[generate] Job: {job_id}", file=sys.stderr)
    print(f"[generate] Size: {job.get('size','?')}, duration: {job.get('seconds','?')}s", file=sys.stderr)
    print(f"[generate] Waiting (typical 30s-4min)...", file=sys.stderr)

    result = poll_job(api_key, job_id)

    outputs = result.get("outputs", {})
    video_url = outputs.get("video_url", "")
    cost = outputs.get("cost", None)
    if not video_url:
        print(f"[generate] ERROR: No video_url in result: {result}", file=sys.stderr)
        sys.exit(2)

    elapsed_total = int(time.time() - job["created_at"]) if "created_at" in job else "?"
    print(f"[generate] Completed in ~{elapsed_total}s. Cost: ${cost if cost else '?'}", file=sys.stderr)
    print(f"[generate] Downloading {video_url}...", file=sys.stderr)

    root = find_project_root()
    out_dir = root / args.output_dir
    slug = slugify(args.prompt)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = f"{slug}-{timestamp}"
    mp4_path = out_dir / f"{base}.mp4"

    size = download_video(video_url, mp4_path)

    print(f"[generate] OK: {mp4_path} ({size/1024/1024:.1f}MB)", file=sys.stderr)
    # Stdout JSON cho parent process (không ghi file metadata)
    print(json.dumps({"video": str(mp4_path), "size_bytes": size, "cost_usd": cost, "model": args.model, "duration": result.get("seconds")}, ensure_ascii=False))


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
