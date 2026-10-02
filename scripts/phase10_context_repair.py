import json
import os
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

RAW = Path("data_cache/phase10_context_raw")
RAW.mkdir(parents=True, exist_ok=True)
OUT = Path("results")
OUT.mkdir(parents=True, exist_ok=True)

START = pd.Timestamp(os.getenv("START_DATE", "2025-01-01")).date()
END = pd.Timestamp(os.getenv("END_DATE", "2026-09-30")).date()
TRADE_DATES = pd.read_csv(OUT / "strategy_v5_trades.csv", usecols=["entry_date"])
TRADE_DATES["entry_date"] = pd.to_datetime(TRADE_DATES["entry_date"]).dt.date


def fetch_fii_history():
    url = "https://raw.githubusercontent.com/MrChartist/fii-dii-data/main/data/history.json"
    path = RAW / "fii_dii_history.json"
    req = Request(url, headers={"User-Agent": "Final-Stand-v4/phase10"})
    with urlopen(req, timeout=60) as resp:
        data = resp.read()
    path.write_bytes(data)
    obj = json.loads(data.decode("utf-8"))
    df = pd.DataFrame(obj)
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
    for c in ["fii_net", "dii_net"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[["date", "fii_net", "dii_net"]].dropna(subset=["date"])
    df = df.drop_duplicates("date", keep="first").sort_values("date")
    df = df[(df["date"] >= pd.Timestamp(START)) & (df["date"] <= pd.Timestamp(END))]
    df.to_csv(RAW / "fii_dii_history.csv", index=False)
    return df


def fetch_nifty_and_vix():
    try:
        from nseindia import NiftyIndicesClient
    except Exception as exc:
        raise RuntimeError("nseindiapy import failed") from exc

    client = NiftyIndicesClient()
    try:
        nifty = client.historical.price_history("NIFTY 50", START, END).to_dicts()
        nifty = pd.DataFrame(nifty)
        nifty["date"] = pd.to_datetime(nifty["date"]).dt.normalize()
        nifty["close"] = pd.to_numeric(nifty["close"], errors="coerce")
        nifty = nifty[["date", "close"]].dropna().drop_duplicates("date").sort_values("date")
        nifty.to_csv(RAW / "nse_nifty50_validated.csv", index=False)

        # India VIX client retrieves NSE daily snapshots. It is slower than a
        # single endpoint call, so it is kept as an explicit validated fallback.
        vix = client.historical.vix_history(START, END).to_dicts()
        vix = pd.DataFrame(vix)
        vix["date"] = pd.to_datetime(vix["date"]).dt.normalize()
        vix["close"] = pd.to_numeric(vix["close"], errors="coerce")
        vix = vix[["date", "close"]].dropna().drop_duplicates("date").sort_values("date")
        vix.to_csv(RAW / "nse_india_vix_validated.csv", index=False)
    finally:
        client.close()


def main():
    fetch_fii_history()
    fetch_nifty_and_vix()

    # Record a compact provenance manifest; normalized CSVs are the cached
    # context inputs used by the lagged join.
    manifest = {
        "phase": 10,
        "status": "validated_context_fallback_acquired",
        "start_date": str(START),
        "end_date": str(END),
        "trade_dates": int(len(TRADE_DATES)),
        "sources": {
            "nifty_vix": "nseindiapy public client using NSE/Nifty Indices historical endpoints and daily snapshots",
            "fii_dii": "MrChartist/fii-dii-data historical JSON, whose pipeline identifies NSE as the source",
        },
        "files": [
            str(RAW / "nse_nifty50_validated.csv"),
            str(RAW / "nse_india_vix_validated.csv"),
            str(RAW / "fii_dii_history.csv"),
        ],
        "policy": "Context is descriptive only; no new trading filter or parameter selection is performed.",
    }
    (OUT / "phase10_context_repair.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps({
        "nifty_rows": len(pd.read_csv(RAW / "nse_nifty50_validated.csv")),
        "vix_rows": len(pd.read_csv(RAW / "nse_india_vix_validated.csv")),
        "fii_dii_rows": len(pd.read_csv(RAW / "fii_dii_history.csv")),
    }, indent=2))


if __name__ == "__main__":
    main()
