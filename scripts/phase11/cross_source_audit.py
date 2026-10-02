#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

IST = "Asia/Kolkata"
PRICE_COLS = [
    ("CE", "ce_otm6"), ("CE", "ce_otm7"), ("CE", "ce_otm8"),
    ("PE", "pe_otm6"), ("PE", "pe_otm7"), ("PE", "pe_otm8"),
]


def ist_ts(value: str) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize(IST) if ts.tzinfo is None else ts.tz_convert(IST)


def load_secondary(root: Path) -> pd.DataFrame:
    frames = []
    for path in sorted((root / "options_secondary").glob("NIFTY_*.parquet")):
        df = pd.read_parquet(path)
        required = {"timestamp", "expiry", "strike", "option_type", "open"}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"{path}: missing {sorted(missing)}")
        df["ts"] = pd.to_datetime(df["timestamp"], errors="coerce")
        if df["ts"].dt.tz is None:
            df["ts"] = df["ts"].dt.tz_localize(IST)
        else:
            df["ts"] = df["ts"].dt.tz_convert(IST)
        df["expiry_date"] = pd.to_datetime(df["expiry"], errors="coerce").dt.date
        df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
        df["open"] = pd.to_numeric(df["open"], errors="coerce")
        df["option_type"] = df["option_type"].astype(str).str.upper()
        frames.append(df[["ts", "expiry_date", "strike", "option_type", "open"]].dropna())
    if not frames:
        raise FileNotFoundError("No secondary NIFTY option files found")
    return pd.concat(frames, ignore_index=True)


def main() -> int:
    root = Path("data_cache/phase11")
    events = pd.read_csv("results/phase11_events.csv")
    events["observation_date"] = pd.to_datetime(events["observation_date"]).dt.date
    events["expiry_date"] = pd.to_datetime(events["expiry_date"]).dt.date
    secondary = load_secondary(root)

    eligible = events[events["observation_date"] >= pd.Timestamp("2024-10-01").date()].copy()
    matched = []
    for _, e in eligible.iterrows():
        ts = ist_ts(e["observation_timestamp_ist"])
        snap = secondary[(secondary["expiry_date"] == e["expiry_date"]) & (secondary["ts"] == ts)]
        if snap.empty:
            continue
        diffs = []
        missing = 0
        for typ, col in PRICE_COLS:
            strike = float(e["atm_strike"]) + (1 if typ == "CE" else -1) * int(col[-1]) * float(e["strike_interval"])
            r = snap[(snap["option_type"] == typ) & np.isclose(snap["strike"], strike, atol=1e-9)]
            if r.empty:
                missing += 1
                continue
            primary = float(e[col])
            secondary_price = float(r.iloc[0]["open"])
            diffs.append({
                "abs": abs(primary - secondary_price),
                "rel": abs(primary - secondary_price) / max(abs(primary), 1e-9),
            })
        if diffs:
            matched.append({
                "expiry_date": str(e["expiry_date"]),
                "observation_date": str(e["observation_date"]),
                "matched_legs": len(diffs),
                "missing_legs": missing,
                "mean_abs_price_diff": float(np.mean([d["abs"] for d in diffs])),
                "median_abs_price_diff": float(np.median([d["abs"] for d in diffs])),
                "mean_relative_price_diff": float(np.mean([d["rel"] for d in diffs])),
            })

    if matched:
        m = pd.DataFrame(matched)
        summary = {
            "eligible_events": int(len(eligible)),
            "events_with_any_secondary_match": int(len(m)),
            "event_match_rate": float(len(m) / len(eligible)),
            "mean_abs_price_diff": float(m["mean_abs_price_diff"].mean()),
            "median_abs_price_diff": float(m["median_abs_price_diff"].median()),
            "mean_relative_price_diff": float(m["mean_relative_price_diff"].mean()),
            "median_relative_price_diff": float(m["mean_relative_price_diff"].median()),
            "events_with_all_six_legs": int((m["matched_legs"] == 6).sum()),
            "all_six_leg_rate_among_eligible": float((m["matched_legs"] == 6).mean()),
        }
    else:
        summary = {
            "eligible_events": int(len(eligible)),
            "events_with_any_secondary_match": 0,
            "event_match_rate": 0.0,
            "mean_abs_price_diff": None,
            "median_abs_price_diff": None,
            "mean_relative_price_diff": None,
            "median_relative_price_diff": None,
            "events_with_all_six_legs": 0,
            "all_six_leg_rate_among_eligible": 0.0,
        }

    Path("results/phase11_cross_source_audit.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
