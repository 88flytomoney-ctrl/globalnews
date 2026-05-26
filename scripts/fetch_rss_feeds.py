#!/usr/bin/env python3
"""
fetch_rss_feeds.py
Fetches and parses RSS feeds for WORLD, BUSINESS, and TECH categories.
"""

import json
import re
import sys
import time
from pathlib import Path

try:
    import feedparser
except ImportError:
    print("feedparser not installed, skipping RSS feeds")
    sys.exit(0)

SCRIPT_DIR = Path(__file__).parent
OUT_FILE   = SCRIPT_DIR.parent / "public" / "data" / "news.json"

RSS_FEEDS = {
    "WORLD": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ],
    "BUSINESS": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
    ],
    "TECH": [
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://techcrunch.com/feed/",
    ],
}


def clean_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def parse_date(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        t = entry.published_parsed
        return f"{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d}"
    return ""


def fetch_feeds():
    news = []
    seen_titles = set()

    for category, feeds in RSS_FEEDS.items():
        for url in feeds:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    title = (entry.get("title") or "").strip()
                    if not title or title in seen_titles:
                        continue
                    seen_titles.add(title)
                    link = entry.get("link") or ""
                    snippet = clean_html(
                        getattr(entry, "summary", "") or getattr(entry, "description", "")
                    )[:200]
                    source = url.split("//")[1].split("/")[0] if "//" in url else url
                    news.append({
                        "category": category,
                        "title": title,
                        "snippet": snippet,
                        "link": link,
                        "date": parse_date(entry),
                        "source": source,
                    })
                time.sleep(0.5)  # be polite
            except Exception as e:
                print(f"  ⚠ {category} ({url}): {e}", file=sys.stderr)

    cat_order = {"WORLD": 0, "BUSINESS": 1, "TECH": 2}
    news.sort(key=lambda x: (cat_order.get(x["category"], 9), x.get("date", ""), -len(x["title"])))
    return news


def main():
    print("=== RSS Feeds ===")
    news = fetch_feeds()
    print(f"  Fetched {len(news)} total news items")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(news, ensure_ascii=False, indent=2))
    print(f"✅ Written {len(news)} items → {OUT_FILE}")


if __name__ == "__main__":
    main()
