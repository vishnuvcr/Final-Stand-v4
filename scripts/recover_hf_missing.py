import json, os
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download
from backtest_v4 import load_spot, expiry_candidates, strikes_for_entry, load_option_window, run_trade

DATA=Path("data_cache"); DATA.mkdir(exist_ok=True)
OUT=Path("results"); OUT.mkdir(exist_ok=True)
HF_REPO=os.getenv("RECOVERY_HF_REPO","thetrademarkk/india-index-options-1m")
QUALITY=Path("results/strategy_v4_data_quality.json")

def download_expiry(ex):
    return Path(hf_hub_download(
        repo_id=HF_REPO,
        filename=f"options/NIFTY/{ex}.parquet",
        repo_type="dataset",
        token=os.getenv("HF_TOKEN"),
        cache_dir=str(DATA/"hf_recovery")
    ))

def main():
    q=json.loads(QUALITY.read_text())
    missing=[x[0] for x in q["skips"] if x[1]=="missing_entry_leg"]
    rows=[]; coverage=[]; errors=[]
    for exs in missing:
        ex=pd.Timestamp(exs).date()
        year=ex.year
        try:
            spot=load_spot(year)
            dates=sorted(pd.Series(spot.timestamp.dt.date.unique()).tolist())
            prev=[d for d in dates if d<ex]
            if len(prev)<4:
                coverage.append({"expiry":str(ex),"status":"not_recoverable","reason":"insufficient_prior_trading_days","source":HF_REPO}); continue
            entry=prev[-4]
            er=spot[(spot.timestamp.dt.date==entry)&(spot.timestamp.dt.hour==10)&(spot.timestamp.dt.minute==0)]
            if er.empty:
                coverage.append({"expiry":str(ex),"status":"not_recoverable","reason":"no_10am_spot","source":HF_REPO}); continue
            t0=pd.Timestamp(entry).replace(hour=10,minute=0)
            exit_ts=pd.Timestamp(ex).replace(hour=15,minute=29)
            entry_spot=float(er.iloc[0].open)
            ks=strikes_for_entry(entry_spot)
            path=download_expiry(ex)
            od=load_option_window(path,ex,t0,exit_ts,list(ks.values()))
            idx={(r.timestamp,float(r.strike),r.option_type):(r.open,r.high,r.low,r.close) for r in od.itertuples(index=False)}
            needed=[(t0,float(ks[k]),"CE" if k.startswith("ce") else "PE") for k in ("ce16","ce17","pe16","pe17")]
            entry_present=all(x in idx and pd.notna(idx[x][0]) and float(idx[x][0])>0 for x in needed)
            exit_needed=[(exit_ts,float(ks[k]),"CE" if k.startswith("ce") else "PE") for k in ("ce16","ce17","pe16","pe17")]
            exit_present=all(x in idx and pd.notna(idx[x][0]) and float(idx[x][0])>0 for x in exit_needed)
            r,reason=run_trade(idx,spot[(spot.timestamp>=t0)&(spot.timestamp<=exit_ts)].copy(),ex)
            if r is not None:
                rows.append(r)
                coverage.append({"expiry":str(ex),"status":"recovered","reason":"","source":HF_REPO,"file":f"options/NIFTY/{ex}.parquet","entry_complete":entry_present,"exit_complete":exit_present,"rows_loaded":len(od)})
            else:
                coverage.append({"expiry":str(ex),"status":"source_present_but_incomplete","reason":reason,"source":HF_REPO,"file":f"options/NIFTY/{ex}.parquet","entry_complete":entry_present,"exit_complete":exit_present,"rows_loaded":len(od)})
        except Exception as exc:
            errors.append({"expiry":str(ex),"error":repr(exc)})
            coverage.append({"expiry":str(ex),"status":"source_unavailable_or_error","reason":repr(exc),"source":HF_REPO})
    pd.DataFrame(rows).to_csv(OUT/"strategy_v4_recovered_trades_hf.csv",index=False)
    pd.DataFrame(coverage).to_csv(OUT/"strategy_v4_recovery_coverage_hf.csv",index=False)
    (OUT/"strategy_v4_recovery_errors_hf.json").write_text(json.dumps(errors,indent=2))
    summary={"source":HF_REPO,"candidates_checked":len(missing),"recovered_trades":len(rows),"errors":len(errors),"coverage":coverage}
    (OUT/"strategy_v4_recovery_summary_hf.json").write_text(json.dumps(summary,indent=2))
    print(json.dumps({"candidates_checked":len(missing),"recovered_trades":len(rows),"errors":len(errors)},indent=2))

if __name__=="__main__":
    main()
