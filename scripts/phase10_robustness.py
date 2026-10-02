import os
import subprocess
import sys
from pathlib import Path
import json
import pandas as pd

ROOT = Path(".")
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

TARGETS = [0.85, 0.90, 0.95, 1.00]
SLIPPAGES = [0.00, 0.10, 0.25, 0.50]
BROKERAGES = [10.0, 20.0, 40.0]


def run_case(target, slippage, brokerage, label):
    env = os.environ.copy()
    env["TARGET_FRAC"] = str(target)
    env["STOP_MULT"] = "0.0"
    env["SLIPPAGE_POINTS"] = str(slippage)
    env["BROKERAGE_PER_ORDER"] = str(brokerage)
    subprocess.run(
        [sys.executable, "scripts/backtest_v5_credit_selected.py"],
        env=env,
        check=True,
    )
    df = pd.read_csv(OUT / "strategy_v5_trades.csv")
    df["phase10_label"] = label
    return df


def summarize(df):
    pnl = df["net_pnl"].astype(float)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    return {
        "trades": int(len(df)),
        "mean_net_pnl": float(pnl.mean()),
        "median_net_pnl": float(pnl.median()),
        "total_net_pnl": float(pnl.sum()),
        "win_rate": float((pnl > 0).mean()),
        "profit_factor": float(wins.sum() / abs(losses.sum())) if len(losses) else None,
        "max_drawdown": float((pnl.cumsum() - pnl.cumsum().cummax()).min()),
        "target_hit_rate": float((df["exit_reason"] == "target").mean()),
        "expiry_rate": float((df["exit_reason"] == "expiry").mean()),
    }


target_rows = []
cost_rows = []
selection_rows = []

for target in TARGETS:
    df = run_case(target, 0.10, 10.0, "target_grid")
    s = summarize(df)
    s["target_fraction"] = target
    target_rows.append(s)

for slippage in SLIPPAGES:
    df = run_case(0.90, slippage, 10.0, "slippage_grid")
    s = summarize(df)
    s["slippage_points"] = slippage
    s["brokerage_per_order"] = 10.0
    cost_rows.append(s)

for brokerage in BROKERAGES:
    df = run_case(0.90, 0.10, brokerage, "brokerage_grid")
    s = summarize(df)
    s["slippage_points"] = 0.10
    s["brokerage_per_order"] = brokerage
    cost_rows.append(s)

# Full Cartesian execution-cost stress: 4 slippage x 3 brokerage scenarios.
for slippage in SLIPPAGES:
    for brokerage in BROKERAGES:
        df = run_case(0.90, slippage, brokerage, "cost_cartesian")
        s = summarize(df)
        s["slippage_points"] = slippage
        s["brokerage_per_order"] = brokerage
        cost_rows.append(s)

pd.DataFrame(target_rows).to_csv(OUT / "phase10_target_sensitivity.csv", index=False)
pd.DataFrame(cost_rows).drop_duplicates(
    subset=["slippage_points", "brokerage_per_order"]
).sort_values(["slippage_points", "brokerage_per_order"]).to_csv(
    OUT / "phase10_cost_stress.csv", index=False
)

base = run_case(0.90, 0.10, 10.0, "baseline")
base["entry_date"] = pd.to_datetime(base["entry_date"])
base["year"] = base["entry_date"].dt.year
base["quarter"] = base["entry_date"].dt.to_period("Q").astype(str)

temporal = []
for (year, quarter, side), g in base.groupby(
    ["year", "quarter", "side"], dropna=False
):
    s = summarize(g)
    s.update({"year": int(year), "quarter": quarter, "side": side})
    temporal.append(s)
pd.DataFrame(temporal).to_csv(OUT / "phase10_temporal_stability.csv", index=False)

# Selection-margin distribution is descriptive only; it is never used as a filter.
if "selection_margin" in base.columns:
    sm = base[["entry_date", "side", "selected_credit", "selection_margin"]].copy()
    sm["selection_margin_quantile"] = pd.qcut(
        sm["selection_margin"], q=4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop"
    )
    sm.to_csv(OUT / "phase10_selection_margin.csv", index=False)

path_cols = [
    "expiry", "entry_date", "side", "net_pnl", "peak_mtm", "trough_mtm",
    "trigger_timestamp", "exit_timestamp", "exit_reason",
    "selected_credit", "selection_margin"
]
base[path_cols].to_csv(OUT / "phase10_path_risk.csv", index=False)

quality = {
    "phase": 10,
    "source_strategy": "Phase 9 frozen V5 credit-selected OTM6/7/8",
    "target_grid": TARGETS,
    "slippage_grid": SLIPPAGES,
    "brokerage_grid": BROKERAGES,
    "full_cartesian_cost_cases": len(SLIPPAGES) * len(BROKERAGES),
    "base_trades": int(len(base)),
    "note": "Market-context acquisition is separate; no context filter is applied."
}
(OUT / "phase10_data_quality.json").write_text(json.dumps(quality, indent=2))
print("Phase 10 computational robustness completed")
