#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.phase11.signal import compute_scores, expiry_return, realized_direction

IST = "Asia/Kolkata"


def to_ist(series: pd.Series) -> pd.Series:
    ts = pd.to_datetime(series, errors="coerce")
    if getattr(ts.dt, "tz", None) is None:
        return ts.dt.tz_localize(IST, ambiguous="NaT", nonexistent="NaT")
    return ts.dt.tz_convert(IST)


def load_options(root: Path) -> pd.DataFrame:
    paths = sorted((root / "options").glob("NIFTY_*.parquet"))
    if not paths:
        raise FileNotFoundError("No cached Phase 11 option parquet files found")
    frames = []
    for path in paths:
        df = pd.read_parquet(path)
        required = {"timestamp", "expiry", "strike", "option_type", "open", "underlying"}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"{path}: missing columns {sorted(missing)}")
        df = df[df["underlying"].astype(str).str.upper().eq("NIFTY")].copy()
        if "granularity" in df.columns:
            df = df[df["granularity"].astype(str).str.lower().str.contains("1m")].copy()
        df["ts"] = to_ist(df["timestamp"])
        df["expiry_date"] = pd.to_datetime(df["expiry"], errors="coerce").dt.date
        df["trade_date"] = df["ts"].dt.date
        df["option_type"] = df["option_type"].astype(str).str.upper()
        df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
        df["open"] = pd.to_numeric(df["open"], errors="coerce")
        frames.append(df.dropna(subset=["ts", "expiry_date", "strike", "open"]))
    return pd.concat(frames, ignore_index=True)


def load_spot(root: Path) -> pd.DataFrame:
    paths = sorted((root / "spot").glob("**/NIFTY50_1min_*.csv"))
    if not paths:
        raise FileNotFoundError("No cached Phase 11 NIFTY spot CSV files found")
    frames = []
    for path in paths:
        df = pd.read_csv(path)
        required = {"Timestamp", "Open", "Close"}
        if not required.issubset(df.columns):
            raise ValueError(f"{path}: expected Timestamp/Open/Close columns")
        df["ts"] = to_ist(df["Timestamp"])
        df["open"] = pd.to_numeric(df["Open"], errors="coerce")
        df["close"] = pd.to_numeric(df["Close"], errors="coerce")
        frames.append(df[["ts", "open", "close"]].dropna(subset=["ts", "open", "close"]))
    out = pd.concat(frames, ignore_index=True).drop_duplicates(subset=["ts"]).sort_values("ts")
    out["trade_date"] = out["ts"].dt.date
    return out


def nearest_strike(strikes: np.ndarray, spot: float) -> float:
    distances = np.abs(strikes - float(spot))
    minimum = distances.min()
    candidates = strikes[np.isclose(distances, minimum, rtol=0.0, atol=1e-9)]
    return float(candidates.max())


def infer_step(strikes: np.ndarray) -> float:
    unique = np.unique(np.sort(strikes.astype(float)))
    diffs = np.diff(unique)
    diffs = diffs[diffs > 0]
    if len(diffs) == 0:
        raise ValueError("Cannot infer strike interval from one strike")
    rounded = np.round(diffs, 6)
    counts = Counter(rounded.tolist())
    return float(sorted(counts, key=lambda x: (-counts[x], x))[0])


def snapshot_price(snapshot: pd.DataFrame, option_type: str, strike: float) -> float | None:
    rows = snapshot[(snapshot["option_type"] == option_type) & np.isclose(snapshot["strike"], strike, atol=1e-9)]
    if rows.empty:
        return None
    return float(rows.iloc[0]["open"])


def build_events(root: Path) -> tuple[pd.DataFrame, dict]:
    options = load_options(root)
    spot = load_spot(root)
    spot_dates = sorted(set(spot["trade_date"]))
    spot_at_10 = spot[spot["ts"].dt.strftime("%H:%M:%S").eq("10:00:00")].copy()
    expiry_dates = sorted(set(options["expiry_date"]))
    rows = []
    skips = Counter()

    for expiry in expiry_dates:
        prior_dates = [d for d in spot_dates if d < expiry]
        if len(prior_dates) < 4:
            skips["not_enough_prior_spot_sessions"] += 1
            continue
        observation_date = prior_dates[-4]
        spot_obs = spot_at_10[spot_at_10["trade_date"].eq(observation_date)]
        if spot_obs.empty:
            skips["missing_10am_spot"] += 1
            continue
        spot_price = float(spot_obs.iloc[0]["open"])

        expiry_close = spot[spot["trade_date"].eq(expiry)]
        if expiry_close.empty:
            skips["missing_expiry_spot"] += 1
            continue
        expiry_value = float(expiry_close.sort_values("ts").iloc[-1]["close"])

        obs_ts = pd.Timestamp(observation_date).tz_localize(IST) + pd.Timedelta(hours=10)
        snapshot = options[(options["expiry_date"].eq(expiry)) & options["ts"].eq(obs_ts)].copy()
        if snapshot.empty:
            skips["missing_10am_option_snapshot"] += 1
            continue

        strikes = np.sort(snapshot["strike"].dropna().unique().astype(float))
        if len(strikes) < 20:
            skips["insufficient_strike_grid"] += 1
            continue
        step = infer_step(strikes)
        atm = nearest_strike(strikes, spot_price)

        target = {
            "CE6": atm + 6 * step,
            "CE7": atm + 7 * step,
            "CE8": atm + 8 * step,
            "PE6": atm - 6 * step,
            "PE7": atm - 7 * step,
            "PE8": atm - 8 * step,
        }
        prices = {
            key: snapshot_price(snapshot, "CE" if key.startswith("CE") else "PE", strike)
            for key, strike in target.items()
        }
        if any(value is None for value in prices.values()):
            skips["missing_required_option"] += 1
            continue

        result = compute_scores(
            prices["CE6"], prices["CE7"], prices["CE8"],
            prices["PE6"], prices["PE7"], prices["PE8"],
        )
        realized = realized_direction(spot_price, expiry_value)
        denominator = abs(result.call_score) + abs(result.put_score)
        rows.append({
            "expiry_date": str(expiry),
            "observation_date": str(observation_date),
            "observation_timestamp_ist": obs_ts.isoformat(),
            "spot_10am": spot_price,
            "expiry_settlement_proxy": expiry_value,
            "point_move": expiry_value - spot_price,
            "expiry_return": expiry_return(spot_price, expiry_value),
            "realized_direction": realized,
            "atm_strike": atm,
            "strike_interval": step,
            "ce_otm6": prices["CE6"],
            "ce_otm7": prices["CE7"],
            "ce_otm8": prices["CE8"],
            "pe_otm6": prices["PE6"],
            "pe_otm7": prices["PE7"],
            "pe_otm8": prices["PE8"],
            "call_score": result.call_score,
            "put_score": result.put_score,
            "spread": result.spread,
            "relative_spread": result.spread / denominator if denominator else np.nan,
            "prediction": result.prediction,
            "prediction_correct": result.prediction == realized if result.prediction != "neutral" else pd.NA,
            "option_price_method": "10:00_bar_open",
            "spot_price_method": "10:00_bar_open",
        })

    events = pd.DataFrame(rows).sort_values(["expiry_date", "observation_date"]).reset_index(drop=True)
    report = {
        "expiry_candidates": len(expiry_dates),
        "events_built": int(len(events)),
        "skips": dict(skips),
        "prediction_counts": events["prediction"].value_counts().to_dict() if not events.empty else {},
        "realized_counts": events["realized_direction"].value_counts().to_dict() if not events.empty else {},
    }
    return events, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data_cache/phase11")
    parser.add_argument("--output", default="results/phase11_events.csv")
    args = parser.parse_args()
    events, report = build_events(Path(args.input))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(output, index=False)
    report_path = output.with_suffix(".json")
    report_path.write_text(json.dumps(report, indent=2, default=str) + "\n")
    print(json.dumps(report, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())