#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

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

    wanted_expiries = set(events["expiry_date"])
    wanted_ts = set(pd.to_datetime(events["observation_timestamp_ist"]))
    df = df[df["expiry_date"].isin(wanted_expiries) & df["ts"].isin(wanted_ts)].copy()
    if df.empty:
        return []

    # Build the six exact target contracts for every eligible event, then
    # perform one vectorized keyed merge rather than row-wise scans.
    targets = []
    for _, e in events.iterrows():
        for typ, col in PRICE_COLS:
            strike = float(e["atm_strike"]) + (1 if typ == "CE" else -1) * int(col[-1]) * float(e["strike_interval"])
            targets.append({
                "expiry_date": e["expiry_date"],
                "ts": pd.Timestamp(e["observation_timestamp_ist"]),
                "option_type": typ,
                "strike": strike,
                "primary_price": float(e[col]),
                "feature": col,
                "event_id": f"{e['expiry_date']}|{e['observation_timestamp_ist']}",
            })
    targets = pd.DataFrame(targets)
    merged = targets.merge(
        df,
        on=["expiry_date", "ts", "option_type", "strike"],
        how="left",
        suffixes=("_primary", "_secondary"),
    )
    merged["abs_diff"] = (merged["primary_price"] - merged["open"]).abs()
    merged["rel_diff"] = merged["abs_diff"] / merged["primary_price"].abs().clip(lower=1e-9)

    out = []
    for event_id, g in merged.groupby("event_id", sort=False):
        valid = g.dropna(subset=["open"])
        if valid.empty:
            continue
        price_map = {
            str(row["feature"]): float(row["open"])
            for _, row in valid.iterrows()
        }
        out.append({
            "event_id": event_id,
            "matched_legs": int(len(valid)),
            "missing_legs": int(6 - len(valid)),
            "mean_abs_price_diff": float(valid["abs_diff"].mean()),
            "median_abs_price_diff": float(valid["abs_diff"].median()),
            "mean_relative_price_diff": float(valid["rel_diff"].mean()),
            "secondary_prices": price_map,
        })
    return out


def main() -> int:
    root = Path("data_cache/phase11")
    events = pd.read_csv("results/phase11_events.csv")
    events["observation_date"] = pd.to_datetime(events["observation_date"]).dt.date
    events["expiry_date"] = pd.to_datetime(events["expiry_date"]).dt.date
    events = events[events["observation_date"] >= pd.Timestamp("2024-10-01").date()].copy()
    events["observation_timestamp_ist"] = pd.to_datetime(
        events["observation_timestamp_ist"]
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

        # Cross-source replication of the two frozen call-wing ratio candidates.
        # Thresholds are taken from the primary-source development sample and
        # are not re-fit on the secondary source.
        dev_primary = events[events["expiry_date"] < pd.Timestamp("2026-01-01").date()].copy()
        thresholds = {
            "ce_otm6_ce_otm7_logratio": float(np.log(dev_primary["ce_otm6"] / dev_primary["ce_otm7"]).median()),
            "ce_otm6_ce_otm8_logratio": float(np.log(dev_primary["ce_otm6"] / dev_primary["ce_otm8"]).median()),
        }
        replication = {}
        full = m[m["matched_legs"] == 6].copy()
        for name, a, b in [
            ("ce_otm6_ce_otm7_logratio", "ce_otm6", "ce_otm7"),
            ("ce_otm6_ce_otm8_logratio", "ce_otm6", "ce_otm8"),
        ]:
            correct = 0
            n = 0
            for _, row in full.iterrows():
                prices = row.get("secondary_prices", {})
                if a not in prices or b not in prices:
                    continue
                ratio = np.log(float(prices[a]) / float(prices[b]))
                pred = "bullish" if ratio >= thresholds[name] else "bearish"
                event_id = str(row["event_id"])
                expiry = event_id.split("|")[0]
                realized = str(events.loc[events["expiry_date"].astype(str).eq(expiry), "realized_direction"].iloc[0])
                n += 1
                correct += int(pred == realized)
            replication[name] = {
                "threshold_from_primary_development": thresholds[name],
                "n": int(n),
                "correct": int(correct),
                "accuracy": float(correct / n) if n else None,
                "exact_binomial_p_50": float(binomtest(correct, n, 0.5).pvalue) if n else None,
            }
        summary["frozen_candidate_replication"] = replication
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
