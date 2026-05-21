#!/usr/bin/env python3
"""
fetch_market_data.py
Fetches live market data and 5-day trend for macro assets.
"""

import json
import sys
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    print("yfinance not installed, skipping market data")
    sys.exit(0)

SCRIPT_DIR = Path(__file__).parent
OUT_FILE   = SCRIPT_DIR.parent / "public" / "data" / "assets.json"

MARKET_ASSETS = {
    "Bitcoin (USD)": "BTC-USD",
    "Gold Futures": "GC=F",
    "Crude Oil WTI": "CL=F",
    "100 HKD to CNY": "HKDCNY=X",
    "100 JPY to HKD": "JPYHKD=X",
    "100 HKD to EUR": "HKDEUR=X",
}


def fetch_market_data():
    results = []
    for name, ticker in MARKET_ASSETS.items():
        try:
            data = yf.Ticker(ticker).history(period="10d")
            if len(data) < 6:
                print(f"  ⚠ {name}: not enough data ({len(data)} rows)", file=sys.stderr)
                continue
            current = float(data["Close"].iloc[-1])
            prev_5d = float(data["Close"].iloc[-6])
            pct = ((current - prev_5d) / prev_5d) * 100
            results.append({
                "name": name,
                "current": round(current, 4),
                "prev5d": round(prev_5d, 4),
                "pctChange": round(pct, 2),
                "isForex": "=X" in ticker,
            })
            print(f"  ✅ {name}: now={current:.2f} 5d={prev_5d:.2f} chg={pct:+.2f}%")
        except Exception as e:
            print(f"  ⚠ {name}: {e}", file=sys.stderr)
    return results


def main():
    print("=== Market Data ===")
    assets = fetch_market_data()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(assets, ensure_ascii=False, indent=2))
    print(f"\n✅ Written {len(assets)} assets → {OUT_FILE}")


if __name__ == "__main__":
    main()
