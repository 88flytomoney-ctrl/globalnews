#!/usr/bin/env python3
"""
fetch_data.py
Orchestrator: runs market + RSS scripts, then assembles feed.json
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
FEED_OUT   = SCRIPT_DIR.parent / "public" / "data" / "feed.json"
ASSETS_OUT = SCRIPT_DIR.parent / "public" / "data" / "assets.json"
NEWS_OUT   = SCRIPT_DIR.parent / "public" / "data" / "news.json"


def run_script(name, script_path):
    print(f"\n▶ Running {name}...")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True, text=True
    )
    if result.stdout:
        print(result.stdout[-800:])
    if result.returncode != 0:
        print(f"  ❌ {name} exited with code {result.returncode}", file=sys.stderr)
        if result.stderr:
            print(result.stderr[-300:], file=sys.stderr)
        return False
    return True


def main():
    ok1 = run_script("market data", SCRIPT_DIR / "fetch_market_data.py")
    ok2 = run_script("RSS feeds",   SCRIPT_DIR / "fetch_rss_feeds.py")

    assets = []
    news   = []

    try:
        assets = json.loads(ASSETS_OUT.read_text())
    except Exception as e:
        print(f"⚠ Could not load assets: {e}", file=sys.stderr)

    try:
        news = json.loads(NEWS_OUT.read_text())
    except Exception as e:
        print(f"⚠ Could not load news: {e}", file=sys.stderr)

    feed = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "assets": assets,
        "news": news,
    }

    FEED_OUT.parent.mkdir(parents=True, exist_ok=True)
    FEED_OUT.write_text(json.dumps(feed, ensure_ascii=False, indent=2))
    print(f"\n✅ feed.json written → {FEED_OUT}")
    print(f"   Assets: {len(assets)}  |  News: {len(news)} items")


if __name__ == "__main__":
    main()
