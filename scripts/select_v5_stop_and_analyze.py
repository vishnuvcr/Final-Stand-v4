import json
from pathlib import Path
import numpy as np
import pandas as pd

OUT=Path('results')
grid=pd.read_csv(OUT/'strategy_v5_trades_grid.csv')
target_grid=pd.read_csv(OUT/'strategy_v5_target_grid.csv')
if grid.empty:
    raise SystemExit('No stop-grid results')

def drawdown(x):
    s=pd.Series(x,dtype=float).reset_index(drop=True)
    eq=s.cumsum()
    return float((eq-eq.cummax()).min()) if len(s) else np.nan

def metrics(df):
    df=df.sort_values('expiry').reset_index(drop=True)
    wins=df[df.net_pnl>0]
    losses=df[df.net_pnl<0]
    pf=float(wins.net_pnl.sum()/abs(losses.net_pnl.sum())) if len(losses) else float('inf')
    return {
        'trades':int(len(df)),
        'mean_net_pnl':float(df.net_pnl.mean()) if len(df) else np.nan,
        'median_net_pnl':float(df.net_pnl.median()) if len(df) else np.nan,
        'total_net_pnl':float(df.net_pnl.sum()),
        'win_rate':float((df.net_pnl>0).mean()) if len(df) else np.nan,
        'profit_factor':pf,
        'max_drawdown':drawdown(df.net_pnl),
        'target_hit_rate':float((df.exit_reason=='target').mean()) if len(df) else np.nan,
        'stop_hit_rate':float((df.exit_reason=='stop').mean()) if len(df) else np.nan,
        'expiry_rate':float((df.exit_reason=='expiry').mean()) if len(df) else np.nan,
        'call_selection_rate':float((df.side=='CALL').mean()) if len(df) else np.nan,
        'put_selection_rate':float((df.side=='PUT').mean()) if len(df) else np.nan
    }

base=grid.sort_values(['expiry','stop_multiple']).reset_index(drop=True)
all_dates=sorted(pd.to_datetime(base.expiry).dt.date.unique().tolist())
n=len(all_dates)
a=int(np.floor(n*0.60)); b=int(np.floor(n*0.80))
dev_dates=set(all_dates[:a]); valid_dates=set(all_dates[a:b]); test_dates=set(all_dates[b:])
valid=base[pd.to_datetime(base.expiry).dt.date.isin(valid_dates)].copy()
selection=[]
for s in sorted(valid.stop_multiple.unique()):
    g=valid[valid.stop_multiple==s]
    m=metrics(g); m['stop_multiple']=float(s); selection.append(m)
sel=pd.DataFrame(selection).sort_values(['mean_net_pnl','median_net_pnl','max_drawdown'],ascending=[False,False,False]).reset_index(drop=True)
chosen=float(sel.iloc[0].stop_multiple)
test=base[(base.stop_multiple==chosen)&(pd.to_datetime(base.expiry).dt.date.isin(test_dates))].copy()

def bootstrap_mean(values,seed=20261002,B=10000):
    arr=np.asarray(values,dtype=float)
    if len(arr)==0: return np.nan,np.nan
    rng=np.random.default_rng(seed)
    sample=rng.choice(arr,size=(B,len(arr)),replace=True).mean(axis=1)
    return float(np.quantile(sample,0.025)),float(np.quantile(sample,0.975))

final=metrics(test)
lo,hi=bootstrap_mean(test.net_pnl)
final.update({'chosen_stop_multiple':chosen,'development_trades':int(sum(pd.to_datetime(base.expiry).dt.date.isin(dev_dates))/len(sorted(base.stop_multiple.unique()))),'validation_trades':int(len(valid)/len(sorted(base.stop_multiple.unique()))),'test_trades':int(len(test)),'bootstrap_mean_95_lo':lo,'bootstrap_mean_95_hi':hi})

sel.to_csv(OUT/'strategy_v5_stop_selection.csv',index=False)
test.to_csv(OUT/'strategy_v5_test_trades.csv',index=False)
(OUT/'strategy_v5_final_summary.json').write_text(json.dumps(final,indent=2))

full_stop=[]
for s,g in base.groupby('stop_multiple'):
    m=metrics(g); m['stop_multiple']=float(s); full_stop.append(m)
pd.DataFrame(full_stop).sort_values('stop_multiple').to_csv(OUT/'strategy_v5_stop_full_sample_sensitivity.csv',index=False)

target_rows=[]
for f,g in target_grid.groupby('target_fraction'):
    m=metrics(g); m['target_fraction']=float(f); target_rows.append(m)
pd.DataFrame(target_rows).sort_values('target_fraction').to_csv(OUT/'strategy_v5_target_sensitivity.csv',index=False)

(OUT/'strategy_v5_selection_meta.json').write_text(json.dumps({
    'development_dates':[str(x) for x in sorted(dev_dates)],
    'validation_dates':[str(x) for x in sorted(valid_dates)],
    'test_dates':[str(x) for x in sorted(test_dates)],
    'chosen_stop_multiple':chosen
},indent=2))
print(json.dumps(final,indent=2))