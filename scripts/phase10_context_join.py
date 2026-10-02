import json
from pathlib import Path
import pandas as pd

OUT = Path("results")
OUT.mkdir(parents=True, exist_ok=True)

trades = pd.read_csv(OUT / "strategy_v5_trades.csv", parse_dates=["entry_date"])
manifest_path = OUT / "phase10_context_acquisition.json"
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"sources": []}


def prior_daily_series(df, date_col, value_col, prefix):
    x = df[[date_col, value_col]].copy()
    x[date_col] = pd.to_datetime(x[date_col], errors="coerce").dt.normalize()
    x[value_col] = pd.to_numeric(x[value_col], errors="coerce")
    x = x.dropna().sort_values(date_col).drop_duplicates(date_col, keep="last")
    x[prefix] = x[value_col]
    return x[[date_col, prefix]]


def read_stooq(path, prefix):
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if "Date" not in df.columns or "Close" not in df.columns:
        return None
    d = pd.DataFrame({
        "date": pd.to_datetime(df["Date"], errors="coerce").dt.normalize(),
        prefix: pd.to_numeric(df["Close"], errors="coerce"),
    }).dropna()
    return d.drop_duplicates("date", keep="last").sort_values("date")


def read_nse_json(path, value_candidates, prefix):
    if not path.exists():
        return None
    try:
        obj = json.loads(path.read_text())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    data = obj.get("data", obj) if isinstance(obj, dict) else obj
    if not isinstance(data, list) or not data:
        return None
    df = pd.DataFrame(data)
    date_col = next((c for c in ["mTIMESTAMP", "TIMESTAMP", "Date", "date"] if c in df.columns), None)
    value_col = next((c for c in value_candidates if c in df.columns), None)
    if not date_col or not value_col:
        return None
    out = pd.DataFrame({
        "date": pd.to_datetime(df[date_col], errors="coerce", dayfirst=True).dt.normalize(),
        prefix: pd.to_numeric(df[value_col].astype(str).str.replace(",", ""), errors="coerce"),
    }).dropna()
    return out.drop_duplicates("date", keep="last").sort_values("date")


def load_fii_dii(path):
    if not path.exists():
        return None
    try:
        obj = json.loads(path.read_text())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    data = obj.get("data", obj) if isinstance(obj, dict) else obj
    if not isinstance(data, list) or not data:
        return None
    df = pd.DataFrame(data)
    date_col = next((c for c in ["date", "Date", "TIMESTAMP"] if c in df.columns), None)
    if not date_col:
        return None
    def pick(*names):
        return next((c for c in names if c in df.columns), None)
    fi = pick("fii_net", "FII/FPI Net", "FII/FPI net", "FII Net")
    di = pick("dii_net", "DII Net", "DII net")
    if not fi and not di:
        return None
    out = pd.DataFrame({"date": pd.to_datetime(df[date_col], errors="coerce", dayfirst=True).dt.normalize()})
    if fi:
        out["fii_net"] = pd.to_numeric(df[fi].astype(str).str.replace(",", ""), errors="coerce")
    if di:
        out["dii_net"] = pd.to_numeric(df[di].astype(str).str.replace(",", ""), errors="coerce")
    return out.dropna(subset=["date"]).drop_duplicates("date", keep="last").sort_values("date")


series = []
nifty = read_nse_json(Path("data_cache/phase10_context_raw/nse_nifty50_history.json"),
                      ["EOD_CLOSE_INDEX_VAL", "CLOSE", "Close", "close"], "nifty_close")
vix = read_nse_json(Path("data_cache/phase10_context_raw/nse_india_vix_history.json"),
                    ["CLOSE", "Close", "close", "EOD_CLOSE_INDEX_VAL"], "india_vix")
fii = load_fii_dii(Path("data_cache/phase10_context_raw/nse_fii_dii.json"))

if nifty is None:
    nifty = read_stooq(Path("data_cache/phase10_context_raw/stooq_nifty.csv"), "nifty_close")
if nifty is not None:
    nifty["nifty_return_1d"] = nifty["nifty_close"].pct_change()
    nifty["nifty_realized_vol_5d"] = nifty["nifty_return_1d"].rolling(5).std() * (252 ** 0.5)
    series.append(nifty)
if vix is not None:
    series.append(vix)
if fii is not None:
    series.append(fii)

for filename, prefix in [
    ("stooq_sp500.csv", "sp500_close"),
    ("stooq_nasdaq.csv", "nasdaq_close"),
    ("stooq_dow.csv", "dow_close"),
    ("stooq_usdinr.csv", "usdinr_close"),
    ("stooq_gold.csv", "gold_close"),
]:
    x = read_stooq(Path("data_cache/phase10_context_raw") / filename, prefix)
    if x is not None:
        x[prefix + "_return_1d"] = x[prefix].pct_change()
        series.append(x)

ctx = pd.DataFrame({"entry_date": trades["entry_date"].dt.normalize()}).drop_duplicates()
# Context is lagged one completed trading day to avoid using same-day closes.
for s in series:
    s = s.copy()
    value_cols = [c for c in s.columns if c != "date"]
    s["context_date"] = s["date"].shift(0)
    s = s.drop(columns=["date"]).rename(columns={"context_date": "date"})
    ctx = pd.merge_asof(
        ctx.sort_values("entry_date"),
        s.sort_values("date"),
        left_on="entry_date",
        right_on="date",
        direction="backward",
        allow_exact_matches=False,
    ).drop(columns=["date"], errors="ignore")

result = trades.merge(ctx, on="entry_date", how="left")
for c in ["nifty_close", "india_vix", "fii_net", "dii_net", "sp500_close", "nasdaq_close",
          "dow_close", "usdinr_close", "gold_close"]:
    if c in result.columns:
        result[c + "_available"] = result[c].notna()

result.to_csv(OUT / "phase10_market_context.csv", index=False)

summary_rows = []
for col in [c for c in result.columns if c.endswith("_available")]:
    summary_rows.append({
        "variable": col.removesuffix("_available"),
        "trades": len(result),
        "available": int(result[col].sum()),
        "coverage_pct": float(result[col].mean() * 100),
    })
pd.DataFrame(summary_rows).to_csv(OUT / "phase10_market_context_summary.csv", index=False)

print("Phase 10 market-context join completed; context is lagged to prior available observation.")
