from pathlib import Path
import pandas as pd
import numpy as np

OUT=Path('results')
trades=pd.read_csv(OUT/'strategy_v4_trades.csv')
if trades.empty:
    raise SystemExit('No trades available for analysis')

def max_drawdown(series):
    eq=series.cumsum()
    dd=eq-eq.cummax()
    return float(dd.min())

wins=trades[trades.net_pnl>0]
losses=trades[trades.net_pnl<0]
profit_factor=float(wins.net_pnl.sum()/abs(losses.net_pnl.sum())) if not losses.empty else np.inf

summary=pd.DataFrame([{
    'strategy':'NIFTY OTM16/17 Double-Sided',
    'trades':len(trades),
    'win_rate':float((trades.net_pnl>0).mean()),
    'mean_net_pnl':float(trades.net_pnl.mean()),
    'median_net_pnl':float(trades.net_pnl.median()),
    'total_net_pnl':float(trades.net_pnl.sum()),
    'gross_total_pnl':float(trades.gross_pnl.sum()),
    'total_costs':float(trades.fees_proxy.sum()),
    'avg_cost_per_trade':float(trades.fees_proxy.mean()),
    'profit_factor':profit_factor,
    'worst_trade':float(trades.net_pnl.min()),
    'best_trade':float(trades.net_pnl.max()),
    'max_sequential_drawdown':max_drawdown(trades.net_pnl),
    'avg_orders':float(trades.orders.mean()),
    'avg_entry_cashflow':float(trades.entry_cashflow.mean())
}])
summary.to_csv(OUT/'strategy_v4_summary.csv',index=False)

monthly=trades.assign(month=pd.to_datetime(trades.expiry).dt.to_period('M').astype(str)).groupby('month').agg(
    trades=('net_pnl','size'),
    total_net_pnl=('net_pnl','sum'),
    mean_net_pnl=('net_pnl','mean'),
    win_rate=('net_pnl',lambda x:float((x>0).mean())),
    total_costs=('fees_proxy','sum')
).reset_index()
monthly.to_csv(OUT/'strategy_v4_monthly.csv',index=False)

yearly=trades.assign(year=pd.to_datetime(trades.expiry).dt.year).groupby('year').agg(
    trades=('net_pnl','size'),
    total_net_pnl=('net_pnl','sum'),
    mean_net_pnl=('net_pnl','mean'),
    median_net_pnl=('net_pnl','median'),
    win_rate=('net_pnl',lambda x:float((x>0).mean())),
    total_costs=('fees_proxy','sum')
).reset_index()
yearly.to_csv(OUT/'strategy_v4_yearly.csv',index=False)

stats=pd.DataFrame([
    {'metric':'n_trades','value':len(trades)},
    {'metric':'mean_net_pnl','value':float(trades.net_pnl.mean())},
    {'metric':'median_net_pnl','value':float(trades.net_pnl.median())},
    {'metric':'std_net_pnl','value':float(trades.net_pnl.std(ddof=1))},
    {'metric':'win_rate','value':float((trades.net_pnl>0).mean())},
    {'metric':'profit_factor','value':profit_factor},
    {'metric':'total_net_pnl','value':float(trades.net_pnl.sum())},
    {'metric':'max_drawdown','value':max_drawdown(trades.net_pnl)}
])
stats.to_csv(OUT/'strategy_v4_statistics.csv',index=False)
print(summary.to_string(index=False))
