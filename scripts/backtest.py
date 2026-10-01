import os, math, json, urllib.request
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

YEARS=[int(x) for x in os.getenv('YEARS','2025,2026').split(',') if x.strip()]
SLIP=float(os.getenv('SLIPPAGE_POINTS','0.10'))
BROKER=float(os.getenv('BROKERAGE_PER_ORDER','10'))
TARGET_FRAC=float(os.getenv('TARGET_FRAC','1.0'))
START=pd.Timestamp(os.getenv('START_DATE','2025-01-01')).date()
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
    s=pd.read_csv(spot_file(y),usecols=['Timestamp','Open','High','Low','Close'])
    s['timestamp']=pd.to_datetime(s['Timestamp'])
    s=s.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
    return s[['timestamp','open','high','low','close']].sort_values('timestamp')

def load_option_window(path, ex, start, end, strikes):
    filters=[('granularity','=','1min'),('expiry','=',str(ex)),('timestamp','>=',pd.Timestamp(start)),('timestamp','<=',pd.Timestamp(end)),('strike','in',[float(x) for x in sorted(set(strikes))])]
    table=pq.read_table(path,columns=['timestamp','expiry','strike','option_type','open','high','low','close'],filters=filters,use_threads=True,pre_buffer=True)
    df=table.to_pandas()
    if df.empty: return df
    df['timestamp']=pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    df['expiry']=pd.to_datetime(df['expiry']).dt.date
    return df.sort_values('timestamp')

def atm(spot): return int(math.floor(float(spot)/50+0.5)*50)
def otm8(spot,side):
    a=atm(spot)
    return a+400 if side=='CE' else a-400
def strike(spot,side,n):
    a=atm(spot)
    return a+n*50 if side=='CE' else a-n*50

def lot_size(ex):
    # NSE revision: 75 remained applicable through the 30-Dec-2025 expiry; 65 thereafter.
    return 75 if pd.Timestamp(ex).date() <= pd.Timestamp('2025-12-30').date() else 65

def exec_px(open_px,action):
    if action in ('BUY','BUYBACK'): return max(0.05,float(open_px)+SLIP)
    return max(0.05,float(open_px)-SLIP)

def run_trade(opt_idx, ss, ex, side):
    t0=pd.Timestamp(ss.iloc[0].timestamp).replace(hour=10,minute=0)
    end=pd.Timestamp(ex).replace(hour=15,minute=29)
    ss=ss[(ss.timestamp>=t0)&(ss.timestamp<=end)].reset_index(drop=True)
    if ss.empty: return None,'no_spot'
    s0=float(ss.iloc[0].close); lot=lot_size(ex)
    ks=[strike(s0,side,6),strike(s0,side,7),strike(s0,side,8)]
    signed={}; cash=0.0; orders=0
    for k,q in zip(ks,[1,-1,-1]):
        r=opt_idx.get((t0,float(k),side))
        if r is None or pd.isna(r[0]) or r[0]<=0: return None,'missing_entry_leg'
        cash += -q*exec_px(r[0],'BUY' if q>0 else 'SELL')*lot
        signed[(float(k),side)]=q; orders+=1
    flatline=cash; target=flatline*TARGET_FRAC; trigger=ks[2]; rolls=0
    exit_reason=None; exit_ts=None; peak=-1e18; trough=1e18
    for i,row in enumerate(ss.itertuples(index=False)):
        ts=row.timestamp
        mtm=0.0
        for (k,typ),q in signed.items():
            r=opt_idx.get((ts,float(k),typ))
            if r is None: mtm=None; break
            mtm += q*float(r[3])*lot
        if mtm is None: continue
        pnl=cash+mtm; peak=max(peak,pnl); trough=min(trough,pnl)
        if ts>t0 and pnl>=target:
            nxt=ss.iloc[i+1] if i+1<len(ss) else None
            if nxt is not None: exit_ts=nxt.timestamp; exit_reason='profit_target'
            else: exit_ts=ts; exit_reason='profit_target_lastbar'
            break
        breach=(float(row.close)>=trigger if side=='CE' else float(row.close)<=trigger)
        if ts>t0 and ts<end and breach and i+1<len(ss):
            nts=ss.iloc[i+1].timestamp
            old=opt_idx.get((nts,float(trigger),side))
            if old is None: return None,'missing_roll_buyback'
            cash -= exec_px(old[0],'BUYBACK')*lot; orders+=1
            signed.pop((float(trigger),side),None)
            newk=otm8(float(row.close),side)
            nr=opt_idx.get((nts,float(newk),side))
            if nr is None: return None,'missing_roll_sell'
            cash += exec_px(nr[0],'SELL')*lot; orders+=1
            signed[(float(newk),side)]=-1; trigger=newk; rolls+=1
    if exit_ts is None: exit_ts=ss.iloc[-1].timestamp; exit_reason='expiry'
    final=cash
    for (k,typ),q in list(signed.items()):
        r=opt_idx.get((exit_ts,float(k),typ))
        if r is None:
            sp=float(ss.iloc[-1].close); intrinsic=max(0,sp-k) if typ=='CE' else max(0,k-sp)
            final += -q*intrinsic*lot
        else:
            final += -q*exec_px(r[0],'SELL' if q>0 else 'BUYBACK')*lot
        orders+=1
    fees=orders*BROKER
    return {'side':side,'expiry':str(ex),'entry_date':str(ss.iloc[0].timestamp.date()),'lot_size':lot,'entry_spot':s0,'otm6':ks[0],'otm7':ks[1],'otm8_initial':ks[2],'flatline':flatline,'target':target,'gross_pnl':final,'fees_proxy':fees,'net_pnl':final-fees,'exit_reason':exit_reason,'exit_ts':str(exit_ts),'rolls':rolls,'orders':orders,'peak_mtm':peak,'trough_mtm':trough},None

def expiry_candidates(spot,year):
    dates=pd.Series(spot.timestamp.dt.date.unique()).sort_values().tolist(); date_set=set(dates)
    start=pd.Timestamp(f'{year}-01-01'); end=pd.Timestamp(f'{year}-12-31')
    tues=pd.date_range(start,end,freq='W-TUE').date
    out=[]
    for t in tues:
        if t in date_set: out.append(t)
        else:
            prev=[d for d in dates if d<t]
            if prev: out.append(prev[-1])
    return sorted(set(out))

def main():
    rows=[]; skips=[]; data_meta=[]
    for y in YEARS:
        print(f'loading spot {y}',flush=True); spot=load_spot(y); path=opt_file(y)
        exps=[e for e in expiry_candidates(spot,y) if START<=e<=END]
        print(f'{y}: {len(exps)} candidate expiries',flush=True)
        for n,ex in enumerate(exps,1):
            entry=(pd.Timestamp(ex)-pd.Timedelta(days=4)).date()
            day=spot[spot.timestamp.dt.date==entry]
            if day.empty: skips.append([str(ex),'entry_not_trading_day']); continue
            window=spot[(spot.timestamp.dt.date>=entry)&(spot.timestamp.dt.date<=ex)]
            if window.empty: skips.append([str(ex),'no_spot_window']); continue
            candidates=set()
            for side in ('CE','PE'):
                candidates.update(strike(float(day.iloc[0].close),side,n) for n in (6,7,8))
                candidates.update(otm8(float(x),side) for x in window.close.tolist())
            start_ts=pd.Timestamp(entry).replace(hour=10,minute=0); end_ts=pd.Timestamp(ex).replace(hour=15,minute=29)
            od=load_option_window(path,ex,start_ts,end_ts,candidates)
            idx={(r.timestamp,float(r.strike),r.option_type):(r.open,r.high,r.low,r.close) for r in od.itertuples(index=False)}
            for side in ('CE','PE'):
                r,e=run_trade(idx,window,ex,side)
                if r: rows.append(r)
                else: skips.append([str(ex),side,e])
            if n%10==0: print(f'{y}: processed {n}/{len(exps)} expiries',flush=True)
        data_meta.append({'year':y,'spot_rows':len(spot),'expiry_candidates':len(exps)})
    res=pd.DataFrame(rows); res.to_csv(OUT/'trades.csv',index=False)
    if not res.empty:
        summary=res.groupby('side').agg(trades=('net_pnl','size'),win_rate=('net_pnl',lambda x:float((x>0).mean())),avg_net=('net_pnl','mean'),median_net=('net_pnl','median'),total_net=('net_pnl','sum'),target_hit=('exit_reason',lambda x:float((x.str.startswith('profit_target')).mean())),avg_rolls=('rolls','mean'),avg_orders=('orders','mean'),avg_fees=('fees_proxy','mean')).reset_index()
    else: summary=pd.DataFrame()
    summary.to_csv(OUT/'summary.csv',index=False)
    quality={'years':YEARS,'trades':len(res),'skips':skips,'per_year':data_meta,'source':'rissin/nse-options-intraday + technovusin/nifty50-historical-data','resolution':'1min','notes':'Option bid/ask unavailable; premium slippage and brokerage are modeled. Expiry dates are generated from Tuesday schedule and actual spot trading dates, then option availability is validated per expiry.'}
    (OUT/'data_quality.json').write_text(json.dumps(quality,indent=2,default=str))
    print(summary.to_string(index=False))

if __name__=='__main__': main()
