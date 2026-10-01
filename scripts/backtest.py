import os, math, json, urllib.request
from pathlib import Path
import pandas as pd
from huggingface_hub import hf_hub_download

YEARS=[int(x) for x in os.getenv('YEARS','2025,2026').split(',') if x.strip()]
LOT=int(os.getenv('LOT_SIZE','65'))
SLIP=float(os.getenv('SLIPPAGE_POINTS','0.10'))
BROKER=float(os.getenv('BROKERAGE_PER_ORDER','20'))
TARGET_FRAC=float(os.getenv('TARGET_FRAC','1.0'))
START=pd.Timestamp(os.getenv('START_DATE','2024-10-01')).date()
END=pd.Timestamp(os.getenv('END_DATE','2026-12-31')).date()
DATA=Path('data_cache'); DATA.mkdir(exist_ok=True)
OUT=Path('results'); OUT.mkdir(exist_ok=True)

def opt_file(y):
    return Path(hf_hub_download(repo_id='rissin/nse-options-intraday', filename=f'upstox_intraday/NIFTY/NIFTY_{y}.parquet', repo_type='dataset', token=os.getenv('HF_TOKEN'), cache_dir=str(DATA)))

def spot_file(y):
    p=DATA/f'NIFTY50_1min_{y}.csv'
    if not p.exists():
        urllib.request.urlretrieve(f'https://raw.githubusercontent.com/technovusin/nifty50-historical-data/main/1min/{y}/NIFTY50_1min_{y}.csv',p)
    return p

def load_spot(y):
    s=pd.read_csv(spot_file(y))
    s['timestamp']=pd.to_datetime(s['Timestamp'])
    s=s.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
    return s[['timestamp','open','high','low','close']].sort_values('timestamp')

def load_options(y):
    cols=['timestamp','expiry','strike','option_type','open','high','low','close','granularity']
    df=pd.read_parquet(opt_file(y),columns=cols,filters=[('granularity','=','1min')])
    df['timestamp']=pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    df['expiry']=pd.to_datetime(df['expiry']).dt.date
    df=df[(df['timestamp'].dt.date>=START)&(df['timestamp'].dt.date<=END)]
    return df.sort_values('timestamp')

def atm(spot): return int(math.floor(float(spot)/50+0.5)*50)
def otm8(spot,side):
    a=atm(spot)
    return a+400 if side=='CE' else a-400
def strike(spot,side,n):
    a=atm(spot)
    return a+n*50 if side=='CE' else a-n*50

def px(idx,ts,ex,k,side):
    r=idx.get((ts,ex,float(k),side))
    return None if r is None else float(r[0])

def exec_px(open_px,action):
    if action in ('BUY','BUYBACK'): return max(0.05,open_px+SLIP)
    return max(0.05,open_px-SLIP)

def run_trade(idx,spot,ex,entry,side):
    t0=pd.Timestamp(entry).replace(hour=10,minute=0)
    end=pd.Timestamp(ex).replace(hour=15,minute=29)
    ss=spot[(spot.timestamp>=t0)&(spot.timestamp<=end)]
    if ss.empty: return None,'no_spot'
    s0=float(ss.iloc[0].close)
    ks=[strike(s0,side,6),strike(s0,side,7),strike(s0,side,8)]
    signed={}
    cash=0.0; orders=0
    for k,q in zip(ks,[1,-1,-1]):
        p=px(idx,t0,ex,k,side)
        if p is None or p<=0: return None,'missing_entry_leg'
        ep=exec_px(p,'BUY' if q>0 else 'SELL')
        signed[(ex,float(k),side)]=q
        cash += -q*ep*LOT
        orders += 1
    flatline=cash; target=flatline*TARGET_FRAC
    trigger=ks[2]; rolls=0; exit_reason=None; exit_ts=None
    peak=-1e18; trough=1e18
    for row in ss.itertuples(index=False):
        ts=row.timestamp
        # MTM using close of the current minute.
        mtm=0.0; missing=False
        for key,q in signed.items():
            r=idx.get((ts,key[0],key[1],key[2]))
            if r is None: missing=True; break
            mtm += q*float(r[3])*LOT
        if missing: continue
        pnl=cash+mtm
        peak=max(peak,pnl); trough=min(trough,pnl)
        if ts>t0 and pnl>=target:
            exit_reason='profit_target'; exit_ts=ts; break
        breach=(float(row.close)>=trigger if side=='CE' else float(row.close)<=trigger)
        if ts>t0 and ts<end and breach:
            nxt=ss[ss.timestamp>ts]
            if nxt.empty: continue
            nts=nxt.iloc[0].timestamp
            old=idx.get((nts,ex,float(trigger),side))
            if old is None: return None,'missing_roll_buyback'
            cash -= exec_px(float(old[0]),'BUYBACK')*LOT; orders+=1
            signed.pop((ex,float(trigger),side),None)
            newk=otm8(float(row.close),side)
            nr=idx.get((nts,ex,float(newk),side))
            if nr is None: return None,'missing_roll_sell'
            cash += exec_px(float(nr[0]),'SELL')*LOT; orders+=1
            signed[(ex,float(newk),side)]=-1
            trigger=newk; rolls+=1
    if exit_reason is None:
        last=ss.iloc[-1]; exit_ts=last.timestamp; exit_reason='expiry'
    # Liquidate all remaining legs at exit-bar open; use intrinsic fallback only if expiry data is absent.
    final=cash
    for key,q in list(signed.items()):
        r=idx.get((exit_ts,key[0],key[1],key[2]))
        if r is None:
            sp=float(ss.iloc[-1].close); k=float(key[1])
            intrinsic=max(0,sp-k) if side=='CE' else max(0,k-sp)
            final += -q*intrinsic*LOT
        else:
            final += -q*exec_px(float(r[0]),'SELL' if q>0 else 'BUYBACK')*LOT
        orders+=1
    turnover_proxy=max(abs(flatline),1.0)
    # Conservative configurable brokerage plus simplified statutory proxy. Exact charge ledger is a Phase 2 refinement.
    fees=orders*BROKER + 0.18*orders*BROKER + 0.001*turnover_proxy
    return {'side':side,'expiry':str(ex),'entry_date':str(entry),'entry_spot':s0,'otm6':ks[0],'otm7':ks[1],'otm8_initial':ks[2],'flatline':flatline,'target':target,'gross_pnl':final,'fees_proxy':fees,'net_pnl':final-fees,'exit_reason':exit_reason,'exit_ts':str(exit_ts),'rolls':rolls,'orders':orders,'peak_mtm':peak,'trough_mtm':trough},None

def main():
    opts=[]; spots=[]
    for y in YEARS:
        print('loading',y,flush=True); opts.append(load_options(y)); spots.append(load_spot(y))
    o=pd.concat(opts,ignore_index=True); s=pd.concat(spots,ignore_index=True).sort_values('timestamp')
    idx={(r.timestamp,r.expiry,float(r.strike),r.option_type):(r.open,r.high,r.low,r.close) for r in o.itertuples(index=False)}
    expiries=sorted(o.expiry.unique()); spot_dates=set(s.timestamp.dt.date)
    rows=[]; skips=[]
    for ex in expiries:
        if ex<START or ex>END: continue
        entry=(pd.Timestamp(ex)-pd.Timedelta(days=4)).date()
        if entry not in spot_dates: skips.append([str(ex),'entry_not_trading_day']); continue
        for side in ('CE','PE'):
            r,e=run_trade(idx,s,ex,entry,side)
            if r: rows.append(r)
            else: skips.append([str(ex),side,e])
    res=pd.DataFrame(rows); res.to_csv(OUT/'trades.csv',index=False)
    if not res.empty:
        summary=res.groupby('side').agg(trades=('net_pnl','size'),win_rate=('net_pnl',lambda x:float((x>0).mean())),avg_net=('net_pnl','mean'),median_net=('net_pnl','median'),total_net=('net_pnl','sum'),target_hit=('exit_reason',lambda x:float((x=='profit_target').mean())),avg_rolls=('rolls','mean'),avg_orders=('orders','mean'),avg_fees=('fees_proxy','mean')).reset_index()
    else: summary=pd.DataFrame()
    summary.to_csv(OUT/'summary.csv',index=False)
    quality={'years':YEARS,'option_rows':len(o),'spot_rows':len(s),'expiries':len(expiries),'trades':len(res),'skips':skips,'source':'rissin/nse-options-intraday + technovusin/nifty50-historical-data','resolution':'1min','notes':'Bid/ask unavailable; slippage and fee model are explicit approximations.'}
    (OUT/'data_quality.json').write_text(json.dumps(quality,indent=2,default=str))
    print(summary.to_string(index=False))

if __name__=='__main__': main()
