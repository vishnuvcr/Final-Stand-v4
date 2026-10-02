import json
import os
import time
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

START = os.getenv("START_DATE", "2025-01-01")
END = os.getenv("END_DATE", "2026-09-30")
RAW = Path("data_cache/phase10_context_raw")
OUT = Path("results")
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)


def get(url, name, headers=None):
    req = Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    path = RAW / name
    try:
        with urlopen(req, timeout=45) as resp:
            data = resp.read()
        path.write_bytes(data)
        return {"status": "ok", "bytes": len(data), "url": url, "file": str(path)}
    except Exception as exc:
        return {"status": "error", "url": url, "error": repr(exc)}


def nse_api(url, name):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json,text/plain,*/*",
        "Referer": "https://www.nseindia.com/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    return get(url, name, headers)


def stooq(symbol, name):
    url = (
        "https://stooq.com/q/d/l/?s="
        + symbol
        + "&d1="
        + START.replace("-", "")
        + "&d2="
        + END.replace("-", "")
        + "&i=d"
    )
    return get(url, name)


records = []

# Official NSE context sources. These endpoints are used only for context, never
# as substitutes for the accepted option ledger.
records.append(nse_api(
    "https://www.nseindia.com/api/historical/indicesHistory"
    "?indexType=NIFTY%2050&from=01-01-2025&to=30-09-2026",
    "nse_nifty50_history.json",
))
records.append(nse_api(
    "https://www.nseindia.com/api/historical/indicesHistory"
    "?indexType=India%20VIX&from=01-01-2025&to=30-09-2026",
    "nse_india_vix_history.json",
))
records.append(nse_api(
    "https://www.nseindia.com/api/fiidiiTradeReact?fromDate=01-01-2025&toDate=30-09-2026",
    "nse_fii_dii.json",
))

# Independent daily validation/context source family for global markets,
# USDINR and gold. These are context variables only.
for symbol, name in [
    ("^spx", "stooq_sp500.csv"),
    ("^ndq", "stooq_nasdaq.csv"),
    ("^dji", "stooq_dow.csv"),
    ("usdinr", "stooq_usdinr.csv"),
    ("xauusd", "stooq_gold.csv"),
]:
    records.append(stooq(symbol, name))
    time.sleep(0.5)

(OUT / "phase10_context_acquisition.json").write_text(
    json.dumps(
        {
            "phase": 10,
            "start_date": START,
            "end_date": END,
            "sources": records,
            "official_nse": [
                "NIFTY 50 historical index data",
                "India VIX historical data",
                "FII/FPI and DII activity",
            ],
            "secondary_validation": [
                "Stooq daily S&P 500",
                "Stooq daily Nasdaq Composite",
                "Stooq daily Dow Jones",
                "Stooq daily USDINR",
                "Stooq daily gold/XAUUSD",
            ],
            "policy": "Context variables are descriptive/explanatory; no new trading filter is created.",
        },
        indent=2,
    )
)

# Normalize successfully acquired CSV context sources when possible.
frames = []
for item in records:
    f = item.get("file")
    if not f or not f.endswith(".csv") or item.get("status") != "ok":
        continue
    try:
        df = pd.read_csv(f)
        if "Date" in df.columns:
            df["date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date.astype("string")
        elif "date" not in df.columns:
            continue
        df["source_file"] = Path(f).name
        frames.append(df)
    except Exception:
        pass

if frames:
    pd.concat(frames, ignore_index=True, sort=False).to_csv(
        OUT / "phase10_context_secondary.csv", index=False
    )

print("Phase 10 market-context acquisition completed with provenance manifest")
