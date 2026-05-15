#!/usr/bin/env python3
"""generate.py - submit VEO 3 generation, poll, download MP4, save local.

Usage:
  python generate.py --prompt "..." [--model X] [--resolution 720p] [--duration 8] [--aspect 16:9]

Reads GEMINI_API_KEY tu .env (priority) hoac .env.local (fallback).
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
API_BASE = "https://generativelanguage.googleapis.com/v1beta"
POLL_INTERVAL = 10
MAX_WAIT = 360  # 6 minutes


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
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip("\"'")
                return key, path
    print(f"[generate] ERROR: GEMINI_API_KEY khong tim thay tai {root}/.env hoac .env.local", file=sys.stderr)
    print(f"[generate] Apply tai https://aistudio.google.com/app/apikey", file=sys.stderr)
    sys.exit(1)


def slugify(s, maxlen=50):
    vn = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
    en = "aaaaaaaaaaaaaaaaaeeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd"
    s = s.lower()
    s = "".join(en[vn.index(c)] if c in vn else c for c in s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:maxlen]


def http_request(url, method="GET", body=None, headers=None):
    headers = headers or {}
    headers.setdefault("User-Agent", UA)
    headers.setdefault("Accept", "application/json")
    if body:
        headers.setdefault("Content-Type", "application/json")
        body = json.dumps(body).encode("utf-8") if not isinstance(body, bytes) else body
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        return urllib.request.urlopen(req, timeout=60)
    except HTTPError as e:
        body_text = e.read().decode()
        print(f"[generate] HTTP {e.code}: {body_text[:500]}", file=sys.stderr)
        raise


def submit_generation(api_key, prompt, model, resolution, duration, aspect):
    url = f"{API_BASE}/models/{model}:predictLongRunning?key={api_key}"
    body = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "aspectRatio": aspect,
            "resolution": resolution,
            "durationSeconds": str(duration),
            "personGeneration": "allow_all",
        },
    }
    resp = http_request(url, method="POST", body=body)
    data = json.loads(resp.read())
    op_name = data.get("name")
    if not op_name:
        print(f"[generate] ERROR: No operation name returned. Response: {data}", file=sys.stderr)
        sys.exit(2)
    return op_name


def poll_operation(api_key, op_name):
    url = f"{API_BASE}/{op_name}?key={api_key}"
    start = time.time()
    last_log = start
    while True:
        elapsed = int(time.time() - start)
        if elapsed > MAX_WAIT:
            print(f"[generate] TIMEOUT after {MAX_WAIT}s waiting for operation done", file=sys.stderr)
            sys.exit(4)

        try:
            resp = http_request(url, method="GET")
            data = json.loads(resp.read())
        except HTTPError:
            time.sleep(POLL_INTERVAL)
            continue

        if data.get("done"):
            return data

        if time.time() - last_log >= 30:
            print(f"[generate] Polling... {elapsed}s elapsed", file=sys.stderr)
            last_log = time.time()

        time.sleep(POLL_INTERVAL)


def download_video(api_key, op_result):
    """Extract video URI tu operation result + download MP4."""
    response = op_result.get("response", {})
    videos = response.get("generatedVideos", [])
    if not videos:
        print(f"[generate] ERROR: No videos in response: {op_result}", file=sys.stderr)
        sys.exit(2)
    video_info = videos[0].get("video", {})
    file_uri = video_info.get("uri", "")
    if not file_uri:
        print(f"[generate] ERROR: No URI in video: {video_info}", file=sys.stderr)
        sys.exit(2)

    # URI format: e.g. "files/abc123" or "gs://..."
    # For Gemini Files API: files/{file_id}, download via:
    if file_uri.startswith("files/"):
        download_url = f"{API_BASE}/{file_uri}?alt=media&key={api_key}"
    else:
        print(f"[generate] WARN: Unexpected URI format: {file_uri}", file=sys.stderr)
        download_url = file_uri

    try:
        req = urllib.request.Request(download_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()
    except HTTPError as e:
        print(f"[generate] Download HTTP {e.code}: {e.read().decode()[:300]}", file=sys.stderr)
        sys.exit(3)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--model", default="veo-3.1-fast-generate-preview")
    p.add_argument("--resolution", default="720p", choices=["720p", "1080p", "4k"])
    p.add_argument("--duration", type=int, default=8, choices=[4, 6, 8])
    p.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"])
    p.add_argument("--output-dir", default="output/videos")
    args = p.parse_args()

    # Validate constraints
    if args.resolution in ("1080p", "4k") and args.duration != 8:
        print(f"[generate] ERROR: {args.resolution} requires duration=8 (API constraint). Got {args.duration}.", file=sys.stderr)
        sys.exit(1)
    if len(args.prompt) < 15:
        print("[generate] ERROR: Prompt qua ngan (<15 chars). Cung cap mo ta chi tiet hon.", file=sys.stderr)
        sys.exit(1)

    api_key, env_path = load_api_key()
    print(f"[generate] API key loaded tu {env_path.name}", file=sys.stderr)
    print(f"[generate] Submitting {args.model} ({args.resolution}, {args.duration}s, {args.aspect})...", file=sys.stderr)

    op_name = submit_generation(api_key, args.prompt, args.model, args.resolution, args.duration, args.aspect)
    print(f"[generate] Operation: {op_name}", file=sys.stderr)
    print(f"[generate] Waiting for completion (typical: fast=11-60s, standard=60-180s, lite=30-90s)...", file=sys.stderr)

    op_result = poll_operation(api_key, op_name)
    print(f"[generate] Operation done. Downloading MP4...", file=sys.stderr)

    video_bytes = download_video(api_key, op_result)
    if len(video_bytes) < 100_000:  # <100KB suspicious
        print(f"[generate] WARN: Video size unusually small ({len(video_bytes)}B)", file=sys.stderr)

    root = find_project_root()
    out_dir = root / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.prompt)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = f"{slug}-{timestamp}"
    mp4_path = out_dir / f"{base}.mp4"
    meta_path = out_dir / f"{base}.json"

    mp4_path.write_bytes(video_bytes)
    meta = {
        "prompt": args.prompt,
        "model": args.model,
        "resolution": args.resolution,
        "duration_seconds": args.duration,
        "aspect_ratio": args.aspect,
        "operation_name": op_name,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "file_size_bytes": len(video_bytes),
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[generate] OK: {mp4_path} ({len(video_bytes)/1024/1024:.1f}MB)", file=sys.stderr)
    print(json.dumps({"video": str(mp4_path), "metadata": str(meta_path), "size_bytes": len(video_bytes)}, ensure_ascii=False))


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
