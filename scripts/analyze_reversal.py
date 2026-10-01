import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import mannwhitneyu

r=pd.read_csv('results/strategy_v3_trades.csv')
out=Path('results'); out.mkdir(exist_ok=True)
rows=[]
rng=np.random.default_rng(42)

for side,g in r.groupby('side'):
    x=g.net_pnl.to_numpy(float)
    boots=np.array([rng.choice(x,len(x),replace=True).mean() for _ in range(5000)])
    lo,hi=np.quantile(boots,[.025,.975])
    wins=int((x>0).sum()); gp=float(x[x>0].sum()); gl=float(-x[x<0].sum())
    rows.append({
        'strategy':g.strategy.iloc[0],'side':side,'trades':len(x),
        'mean':x.mean(),'median':np.median(x),'win_rate':(x>0).mean(),
        'profit_factor':gp/gl if gl else np.inf,'total':x.sum(),'std':x.std(ddof=1),
        'max_loss':x.min(),'bootstrap_mean_lo':lo,'bootstrap_mean_hi':hi,
        'roll_rate':g.rolls.mean(),'avg_orders':g.orders.mean(),
        'total_fees':g.fees_proxy.sum(),'avg_fees':g.fees_proxy.mean()
    })
s=pd.DataFrame(rows)
s.to_csv(out/'strategy_v3_statistics.csv',index=False)

if set(r.side)=={'CE','PE'}:
    ce=r[r.side=='CE'].set_index('expiry').net_pnl
    pe=r[r.side=='PE'].set_index('expiry').net_pnl
    z=pd.concat([ce,pe],axis=1,keys=['CE','PE']).dropna()
    u,p=mannwhitneyu(ce,pe,alternative='two-sided')
    paired=z.CE-z.PE
    perm=np.array([np.mean(paired.to_numpy()*rng.choice([-1,1],len(paired))) for _ in range(10000)])
    obs=float(paired.mean()); pp=float((np.abs(perm)>=abs(obs)).mean())
    pd.DataFrame([{'aligned_trades':len(z),'mann_whitney_u':u,
                   'mann_whitney_p':p,'paired_mean_difference':obs,
                   'paired_sign_permutation_p':pp}]).to_csv(
        out/'strategy_v3_call_put_tests.csv',index=False)

    metrics=[]
    for metric in ['trades','mean','median','win_rate','profit_factor','total','std',
                   'max_loss','roll_rate','avg_orders','total_fees','avg_fees']:
        a=float(s.loc[s.side=='CE',metric].iloc[0])
        b=float(s.loc[s.side=='PE',metric].iloc[0])
        metrics.append({'metric':metric,'CE':a,'PE':b,
                        'CE_to_PE_ratio':(a/b if b!=0 else np.nan),
                        'CE_minus_PE':a-b})
    pd.DataFrame(metrics).to_csv(out/'strategy_v3_call_put_comparison.csv',index=False)

for side,g in r.sort_values('expiry').groupby('side'):
    eq=g.net_pnl.cumsum(); dd=eq-eq.cummax()
    pd.DataFrame({'expiry':g.expiry,'equity':eq,'drawdown':dd}).to_csv(
        out/f'strategy_v3_equity_{side}.csv',index=False)

r['expiry']=pd.to_datetime(r['expiry'])
monthly=(r.assign(month=r.expiry.dt.to_period('M').astype(str))
    .groupby(['month','side']).net_pnl.agg(['count','sum','mean']).reset_index())
monthly.to_csv(out/'strategy_v3_monthly.csv',index=False)
