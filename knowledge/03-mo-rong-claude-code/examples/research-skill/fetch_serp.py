"""
Fetch top SERP results từ SerpAPI cho 1 chủ đề.

Usage:
    python fetch_serp.py "<chủ đề>" [--top N] [--lang vi] [--country vn]

Output:
    output/serp-<chủ đề>.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: cần cài requests. Chạy: pip install requests")
    sys.exit(1)


def fetch_serp(query: str, top: int = 10, lang: str = "vi", country: str = "vn") -> dict:
    api_key = os.environ.get("SERPAPI_KEY")
    if not api_key:
        raise SystemExit("ERROR: chưa set SERPAPI_KEY trong .env")

    response = requests.get(
        "https://serpapi.com/search",
        params={
            "q": query,
            "api_key": api_key,
            "hl": lang,
            "gl": country,
            "num": top,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def extract_organic(data: dict, top: int) -> list[dict]:
    """Lấy top N organic results, simplify."""
    results = data.get("organic_results", [])[:top]
    return [
        {
            "position": r.get("position"),
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet"),
            "domain": r.get("displayed_link", "").split("/")[0],
        }
        for r in results
    ]


def main():
    parser = argparse.ArgumentParser(description="Fetch SERP results.")
    parser.add_argument("query", help="Chủ đề cần research")
    parser.add_argument("--top", type=int, default=10, help="Số kết quả top (default: 10)")
    parser.add_argument("--lang", default="vi", help="Ngôn ngữ (default: vi)")
    parser.add_argument("--country", default="vn", help="Quốc gia (default: vn)")
    args = parser.parse_args()

    print(f"Fetching SERP cho: '{args.query}' (top {args.top}, {args.lang}-{args.country})...")
    data = fetch_serp(args.query, args.top, args.lang, args.country)
    organic = extract_organic(data, args.top)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    safe_name = "".join(c if c.isalnum() else "-" for c in args.query.lower()).strip("-")
    filename = output_dir / f"serp-{safe_name}.json"

    payload = {
        "query": args.query,
        "fetched_at": datetime.now().isoformat(),
        "top": args.top,
        "lang": args.lang,
        "country": args.country,
        "results": organic,
    }

    filename.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {filename}")
    print(f"Top {len(organic)} results:")
    for r in organic[:5]:
        print(f"  {r['position']}. {r['title']} ({r['domain']})")


if __name__ == "__main__":
    main()
