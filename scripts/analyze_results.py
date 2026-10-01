import pandas as pd, numpy as np, json
from pathlib import Path
from scipy.stats import mannwhitneyu

r=pd.read_csv("results/trades.csv")
out=Path("results"); out.mkdir(exist_ok=True)
rows=[]
rng=np.random.default_rng(42)
for side,g in r.groupby("side"):
    x=g.net_pnl.to_numpy(float)
    boots=[]
    for _ in range(5000):
        boots.append(rng.choice(x,len(x),replace=True).mean())
    q=np.quantile(boots,[.025,.975])
    wins=(x>0).sum(); losses=(x<0).sum()
    gp=x[x>0].sum(); gl=-x[x<0].sum()
    rows.append(dict(side=side,trades=len(x),mean=x.mean(),median=np.median(x),
                    win_rate=(x>0).mean(),profit_factor=gp/gl if gl else np.inf,
                    total=x.sum(),std=x.std(ddof=1),max_loss=x.min(),
                    bootstrap_mean_lo=q[0],bootstrap_mean_hi=q[1],
                    target_hit=(g.exit_reason=="profit_target").mean(),
                    expiry_exit=(g.exit_reason=="expiry").mean(),
                    avg_rolls=g.rolls.mean(),max_rolls=g.rolls.max()))
s=pd.DataFrame(rows)
s.to_csv(out/"statistics.csv",index=False)
if set(r.side)=={"CE","PE"}:
    ce=r[r.side=="CE"].set_index("expiry").net_pnl
    pe=r[r.side=="PE"].set_index("expiry").net_pnl
    z=pd.concat([ce,pe],axis=1,keys=["CE","PE"]).dropna()
    u,p=mannwhitneyu(ce,pe,alternative="two-sided")
    paired=z.CE-z.PE
    perm=[]
    for _ in range(10000):
        signs=rng.choice([-1,1],len(paired))
        perm.append(np.mean(paired.to_numpy()*signs))
    obs=paired.mean()
    pp=(np.abs(perm)>=abs(obs)).mean()
    pd.DataFrame([dict(aligned_trades=len(z),mann_whitney_u=u,mann_whitney_p=p,
                       paired_mean_difference=obs,paired_sign_permutation_p=pp)]).to_csv(out/"call_put_tests.csv",index=False)
# simple equity curves and drawdowns, by side
for side,g in r.sort_values("expiry").groupby("side"):
    eq=g.net_pnl.cumsum()
    dd=eq-eq.cummax()
    pd.DataFrame({"expiry":g.expiry,"equity":eq,"drawdown":dd}).to_csv(out/f"equity_{side}.csv",index=False)
