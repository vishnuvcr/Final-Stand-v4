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


def normalize_ts(series: pd.Series) -> pd.Series:
    ts = pd.to_datetime(series, errors="coerce")
    if ts.dt.tz is None:
        return ts.dt.tz_localize(IST)
    return ts.dt.tz_convert(IST)


def audit_file(path: Path, events: pd.DataFrame) -> list[dict]:
    # Stream one year at a time to avoid holding the multi-year secondary
    # archive alongside the primary archive in memory.
    df = pd.read_parquet(
        path,
        columns=["timestamp", "expiry", "strike", "option_type", "open"],
    )
    df["ts"] = normalize_ts(df["timestamp"])
    df["expiry_date"] = pd.to_datetime(df["expiry"], errors="coerce").dt.date
    df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
    df["open"] = pd.to_numeric(df["open"], errors="coerce")
    df["option_type"] = df["option_type"].astype(str).str.upper()
    df = df.dropna(subset=["ts", "expiry_date", "strike", "open"])

    event_keys = set(zip(events["expiry_date"], events["observation_timestamp_ist"]))
    df = df[df.apply(lambda r: (r["expiry_date"], r["ts"].isoformat()) in event_keys, axis=1)]
    if df.empty:
        return []

    out = []
    for _, e in events.iterrows():
        snap = df[
            (df["expiry_date"] == e["expiry_date"])
            & (df["ts"] == pd.Timestamp(e["observation_timestamp_ist"]))
        ]
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
            out.append({
                "expiry_date": str(e["expiry_date"]),
                "observation_date": str(e["observation_date"]),
                "matched_legs": len(diffs),
                "missing_legs": missing,
                "mean_abs_price_diff": float(np.mean([d["abs"] for d in diffs])),
                "median_abs_price_diff": float(np.median([d["abs"] for d in diffs])),
                "mean_relative_price_diff": float(np.mean([d["rel"] for d in diffs])),
            })
    return out


def main() -> int:
    root = Path("data_cache/phase11")
    events = pd.read_csv("results/phase11_events.csv")
    events["observation_date"] = pd.to_datetime(events["observation_date"]).dt.date
    events["expiry_date"] = pd.to_datetime(events["expiry_date"]).dt.date
    events = events[events["observation_date"] >= pd.Timestamp("2024-10-01").date()].copy()
    events["observation_timestamp_ist"] = events["observation_timestamp_ist"].map(
        lambda x: pd.Timestamp(x).isoformat()
    )

    matched = []
    for path in sorted((root / "options_secondary").glob("NIFTY_*.parquet")):
        matched.extend(audit_file(path, events))

    if matched:
        m = pd.DataFrame(matched)
        summary = {
            "eligible_events": int(len(events)),
            "events_with_any_secondary_match": int(len(m)),
            "event_match_rate": float(len(m) / len(events)),
            "mean_abs_price_diff": float(m["mean_abs_price_diff"].mean()),
            "median_abs_price_diff": float(m["median_abs_price_diff"].median()),
            "mean_relative_price_diff": float(m["mean_relative_price_diff"].mean()),
            "median_relative_price_diff": float(m["mean_relative_price_diff"].median()),
            "events_with_all_six_legs": int((m["matched_legs"] == 6).sum()),
            "all_six_leg_rate_among_matched": float((m["matched_legs"] == 6).mean()),
        }
    else:
        summary = {
            "eligible_events": int(len(events)),
            "events_with_any_secondary_match": 0,
            "event_match_rate": 0.0,
            "mean_abs_price_diff": None,
            "median_abs_price_diff": None,
            "mean_relative_price_diff": None,
            "median_relative_price_diff": None,
            "events_with_all_six_legs": 0,
            "all_six_leg_rate_among_matched": 0.0,
        }

    Path("results/phase11_cross_source_audit.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
