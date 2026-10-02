import json, os, subprocess, sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"backtest_v5_credit_selected.py"
OUT=ROOT/"results"
OUT.mkdir(exist_ok=True)
TARGET="0.90"
CANDIDATES=(
    [("fixed",x) for x in (50,75,100,125,150,200)] +
    [("pct",x) for x in (0.0025,0.0040,0.0050,0.0075,0.0100)] +
    [("atr",x) for x in (0.50,0.75,1.00,1.25,1.50)]
)

def patched_source():
    s=BASE.read_text()
    s=s.replace("STOP_MULT=float(os.getenv('STOP_MULT','0'))",
                "STOP_MULT=float(os.getenv('STOP_MULT','0'))\nSPOT_STOP_KIND=os.getenv('SPOT_STOP_KIND','none')\nSPOT_STOP_VALUE=float(os.getenv('SPOT_STOP_VALUE','0'))")
    marker="    trigger=None; trigger_type=None; trigger_value=None; peak=-1e18; trough=1e18\n"
    inject="""    # Spot barrier is defined from information available before entry.
    daily=spot.assign(date=spot.timestamp.dt.date).groupby('date').agg(open=('open','first'),high=('high','max'),low=('low','min'),close=('close','last')).reset_index()
    prior=daily[daily['date'] < entry]
    atr_value=np.nan
    if len(prior)>=15:
        prev_close=prior['close'].shift(1)
        tr=pd.concat([(prior['high']-prior['low']).rename('a'),(prior['high']-prev_close).abs().rename('b'),(prior['low']-prev_close).abs().rename('c')],axis=1).max(axis=1)
        atr_value=float(tr.tail(14).mean())
    if SPOT_STOP_KIND=='fixed':
        spot_barrier=entry_spot + SPOT_STOP_VALUE if side=='PUT' else entry_spot - SPOT_STOP_VALUE
    elif SPOT_STOP_KIND=='pct':
        spot_barrier=entry_spot*(1.0+SPOT_STOP_VALUE) if side=='PUT' else entry_spot*(1.0-SPOT_STOP_VALUE)
    elif SPOT_STOP_KIND=='atr':
        spot_barrier=entry_spot + SPOT_STOP_VALUE*atr_value if side=='PUT' else entry_spot - SPOT_STOP_VALUE*atr_value
    else:
        spot_barrier=np.nan
"""
    s=s.replace(marker, marker+inject)
    old="""        if STOP_MULT>0 and m<=stop_rupees:
            trigger=t; trigger_type='stop'; trigger_value=m; break
        if m>=target_rupees:
"""
    new="""        if SPOT_STOP_KIND != 'none' and pd.notna(spot_barrier):
            sr=spot.loc[spot.timestamp==t,'close']
            if len(sr):
                current_spot=float(sr.iloc[0])
                adverse=(current_spot >= spot_barrier) if side=='PUT' else (current_spot <= spot_barrier)
                if adverse:
                    trigger=t; trigger_type='spot_stop'; trigger_value=m; break
        if m>=target_rupees:
"""
    if old not in s: raise RuntimeError("base stop block not found")
    s=s.replace(old,new)
    return s

def run_candidate(kind,value):
    label=f"{kind}_{str(value).replace('.','p')}"
    d=OUT/"phase11_runs"/label
    d.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    env.update({"TARGET_FRAC":TARGET,"STOP_MULT":"0","SPOT_STOP_KIND":kind,"SPOT_STOP_VALUE":str(value),
                "OUT_DIR":str(d),"START_DATE":"2025-01-01","END_DATE":"2026-09-30"})
    code=patched_source()+"\n"
    p=subprocess.run([sys.executable,"-c",code],cwd=ROOT,env=env,text=True,capture_output=True)
    if p.returncode:
        raise RuntimeError(f"{label}: {p.stderr[-4000:]}")
    f=d/"strategy_v5_trades.csv"
    if not f.exists(): raise RuntimeError(f"{label}: missing trade output")
    return label,p.stdout[-1000:]

def metrics(df):
    x=df['net_pnl'].astype(float)
    wins=(x>0).sum(); losses=x[x<0]
    pf=float(x[x>0].sum()/abs(losses.sum())) if len(losses) else float('inf')
    return {"trades":int(len(x)),"mean_net_pnl":float(x.mean()) if len(x) else np.nan,
            "median_net_pnl":float(x.median()) if len(x) else np.nan,"total_net_pnl":float(x.sum()) if len(x) else 0.0,
            "win_rate":float((x>0).mean()) if len(x) else np.nan,"profit_factor":pf,
            "max_drawdown":float(x.cumsum().sub(x.cumsum().cummax()).min()) if len(x) else np.nan,
            "target_hit_rate":float((df.exit_reason=='target').mean()) if len(x) else np.nan,
            "spot_stop_rate":float((df.exit_reason=='spot_stop').mean()) if len(x) else np.nan,
            "expiry_rate":float((df.exit_reason=='expiry').mean()) if len(x) else np.nan}

def main():
    run_meta=[]
    for kind,val in CANDIDATES:
        label,_=run_candidate(kind,val)
        df=pd.read_csv(OUT/"phase11_runs"/label/"strategy_v5_trades.csv")
        df['entry_date']=pd.to_datetime(df['entry_date']).dt.date
        run_meta.append((label,kind,val,df))
    sel=pd.read_json(ROOT/"results"/"strategy_v5_selection_meta.json")
    # JSON lists are easiest read directly.
    meta=json.loads((ROOT/"results"/"strategy_v5_selection_meta.json").read_text())
    dev=set(pd.to_datetime(meta["development_dates"]).date); val=set(pd.to_datetime(meta["validation_dates"]).date); test=set(pd.to_datetime(meta["test_dates"]).date)
    rows=[]
    for label,kind,val,df in run_meta:
        d=df[df.entry_date.isin(dev)]; v=df[df.entry_date.isin(val)]; t=df[df.entry_date.isin(test)]
        m=metrics(v); tm=metrics(t)
        rows.append({"label":label,"kind":kind,"value":val,**{f"validation_{k}":v for k,v in m.items()},**{f"test_{k}":v for k,v in tm.items()}})
    grid=pd.DataFrame(rows)
    grid.to_csv(OUT/"phase11_candidate_grid.csv",index=False)
    valid=grid.sort_values(["validation_mean_net_pnl","validation_median_net_pnl","validation_max_drawdown"],ascending=[False,False,False])
    chosen=valid.iloc[0]
    chosen_label=str(chosen["label"])
    chosen_kind=str(chosen["kind"]); chosen_value=float(chosen["value"])
    selected=grid[grid.label==chosen_label].copy()
    selected.to_csv(OUT/"phase11_validation_selection.csv",index=False)
    final_df=next(df for label,kind,val,df in run_meta if label==chosen_label)
    test_df=final_df[final_df.entry_date.isin(test)].copy()
    test_df.to_csv(OUT/"phase11_test_trades.csv",index=False)
    summary={"chosen_label":chosen_label,"chosen_kind":chosen_kind,"chosen_value":chosen_value,
             "selection_rule":"validation mean net P&L; tie-break median net P&L then max drawdown",
             "validation":metrics(final_df[final_df.entry_date.isin(val)]),"untouched_test":metrics(test_df),
             "candidate_count":len(CANDIDATES),"control_no_spot_stop":"Phase 9 0x/no-stop remains the frozen control",
             "note":"No candidate was selected using the untouched test."}
    (OUT/"phase11_final_summary.json").write_text(json.dumps(summary,indent=2,default=str))
    quality={"candidate_families":{"fixed_points":[50,75,100,125,150,200],"percent":[0.0025,0.004,0.005,0.0075,0.01],"atr":[0.5,0.75,1,1.25,1.5]},
             "target_fraction":0.90,"development_n":len(dev),"validation_n":len(val),"test_n":len(test),"completed_candidates":len(CANDIDATES)}
    (OUT/"phase11_data_quality.json").write_text(json.dumps(quality,indent=2))
    print(json.dumps(summary,indent=2,default=str))

if __name__=="__main__":
    main()
