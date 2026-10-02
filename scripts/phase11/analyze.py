#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def logistic_irls(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float, float]:
    X = np.column_stack([np.ones(len(x)), x])
    beta = np.zeros(2)
    for _ in range(100):
        z = np.clip(X @ beta, -30, 30)
        p = 1.0 / (1.0 + np.exp(-z))
        w = p * (1.0 - p)
        info = X.T @ (w[:, None] * X)
        grad = X.T @ (y - p)
        step = np.linalg.solve(info, grad)
        beta += step
        if np.max(np.abs(step)) < 1e-10:
            break
    z = np.clip(X @ beta, -30, 30)
    p = 1.0 / (1.0 + np.exp(-z))
    info = X.T @ ((p * (1.0 - p))[:, None] * X)
    cov = np.linalg.inv(info)
    se = float(np.sqrt(cov[1, 1]))
    return float(beta[0]), float(beta[1]), se, float(beta[1] / se)


def bootstrap_accuracy(values: np.ndarray, seed: int = 20261002, n_boot: int = 20000) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(n_boot, len(values)), replace=True).mean(axis=1)
    return tuple(np.quantile(samples, [0.025, 0.975]))


def summarize(df: pd.DataFrame) -> dict:
    correct = df["prediction_correct"].astype(bool).to_numpy()
    accuracy = float(correct.mean())
    bt_lo, bt_hi = bootstrap_accuracy(correct.astype(float))
    bt = stats.binomtest(int(correct.sum()), len(correct), 0.5)
    always_bullish = float((df["realized_direction"] == "bullish").mean())
    always_bearish = float((df["realized_direction"] == "bearish").mean())

    x = df["spread"].to_numpy(float)
    yret = df["expiry_return"].to_numpy(float)
    y = (df["realized_direction"] == "bullish").astype(int).to_numpy()
    pear = stats.pearsonr(x, yret)
    spear = stats.spearmanr(x, yret)
    intercept, slope, slope_se, slope_z = logistic_irls(x, y)
    slope_p = float(2 * stats.norm.sf(abs(slope_z)))

    return {
        "n": int(len(df)),
        "correct": int(correct.sum()),
        "accuracy": accuracy,
        "accuracy_bootstrap_95ci": [float(bt_lo), float(bt_hi)],
        "accuracy_exact_binomial_p": float(bt.pvalue),
        "always_bullish_baseline": always_bullish,
        "always_bearish_baseline": always_bearish,
        "mean_expiry_return": float(yret.mean()),
        "median_expiry_return": float(np.median(yret)),
        "pearson_spread_return": {"r": float(pear.statistic), "p": float(pear.pvalue)},
        "spearman_spread_return": {"rho": float(spear.statistic), "p": float(spear.pvalue)},
        "logistic_realized_bullish_on_spread": {
            "intercept": intercept,
            "slope": slope,
            "slope_se": slope_se,
            "z": slope_z,
            "p": slope_p,
            "ci95": [slope - 1.96 * slope_se, slope + 1.96 * slope_se],
            "odds_ratio_per_one_spread_unit": float(np.exp(slope)),
        },
        "prediction_counts": df["prediction"].value_counts().to_dict(),
        "realized_counts": df["realized_direction"].value_counts().to_dict(),
    }


def main() -> int:
    p = Path("results/phase11_events.csv")
    df = pd.read_csv(p)
    df["prediction_correct"] = df["prediction_correct"].astype(str).str.lower().eq("true")
    df["expiry_return"] = pd.to_numeric(df["expiry_return"])
    df["spread"] = pd.to_numeric(df["spread"])
    df["expiry_date"] = pd.to_datetime(df["expiry_date"])

    overall = summarize(df)
    train = df[df["expiry_date"] < "2026-01-01"]
    holdout = df[df["expiry_date"] >= "2026-01-01"]

    dec = df.sort_values("spread").reset_index(drop=True)
    decile_rows = []
    for i, g in dec.groupby(pd.qcut(np.arange(len(dec)), 10, labels=False)):
        decile_rows.append({
            "decile": int(i) + 1,
            "n": int(len(g)),
            "accuracy": float(g["prediction_correct"].mean()),
            "mean_expiry_return": float(g["expiry_return"].mean()),
        })

    out = {
        "protocol": {
            "primary_snapshot": "10:00:00 IST one-minute bar OPEN",
            "expiry_value": "latest available NIFTY CLOSE on expiry date",
            "direction_mapping": "call_score > put_score => bearish; put_score > call_score => bullish",
            "holdout_boundary": "2026-01-01",
            "bootstrap_seed": 20261002,
        },
        "overall": overall,
        "development_2024_2025": summarize(train),
        "holdout_2026": summarize(holdout),
        "spread_deciles": decile_rows,
        "confusion_matrix": {
            "bullish_prediction_bullish_realized": int(((df.prediction == "bullish") & (df.realized_direction == "bullish")).sum()),
            "bullish_prediction_bearish_realized": int(((df.prediction == "bullish") & (df.realized_direction == "bearish")).sum()),
            "bearish_prediction_bullish_realized": int(((df.prediction == "bearish") & (df.realized_direction == "bullish")).sum()),
            "bearish_prediction_bearish_realized": int(((df.prediction == "bearish") & (df.realized_direction == "bearish")).sum()),
        },
    }
    Path("results/phase11_statistical_analysis.json").write_text(json.dumps(out, indent=2) + "\n")

    md = [
        "# Phase 11 Statistical Analysis",
        "",
        f"- Events: {overall['n']}",
        f"- Correct predictions: {overall['correct']}",
        f"- Accuracy: {overall['accuracy']:.4f}",
        f"- Exact binomial p-value vs 50%: {overall['accuracy_exact_binomial_p']:.6f}",
        f"- Bootstrap 95% CI: {overall['accuracy_bootstrap_95ci'][0]:.4f} to {overall['accuracy_bootstrap_95ci'][1]:.4f}",
        f"- Always-bullish baseline: {overall['always_bullish_baseline']:.4f}",
        f"- Always-bearish baseline: {overall['always_bearish_baseline']:.4f}",
        f"- Pearson spread/expiry-return r: {overall['pearson_spread_return']['r']:.4f} (p={overall['pearson_spread_return']['p']:.6f})",
        f"- Logistic slope: {overall['logistic_realized_bullish_on_spread']['slope']:.6f} (p={overall['logistic_realized_bullish_on_spread']['p']:.6f})",
        f"- 2024–2025 development accuracy: {out['development_2024_2025']['accuracy']:.4f}",
        f"- 2026 holdout accuracy: {out['holdout_2026']['accuracy']:.4f}",
        "",
        "## Interpretation",
        "",
        "This is a descriptive/statistical Phase 3 result, not a trading recommendation. The primary directional test is judged against the pre-specified 50% null and the chronological 2026 holdout. Trading translation remains blocked until robustness and execution-cost analysis are completed.",
    ]
    Path("results/phase11_statistical_analysis.md").write_text("\n".join(md) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
