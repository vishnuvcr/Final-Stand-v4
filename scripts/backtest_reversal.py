import os, math, json, urllib.request
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

YEARS=[int(x) for x in os.getenv('YEARS','2025,2026').split(',') if x.strip()]
SLIP=float(os.getenv('SLIPPAGE_POINTS','0.10'))
BROKER=float(os.getenv('BROKERAGE_PER_ORDER','20'))
EXCHANGE_RATE=float(os.getenv('NSE_OPTIONS_EXCHANGE_RATE','0.0003503'))
EXCHANGE_RATE_2026=float(os.getenv('NSE_OPTIONS_EXCHANGE_RATE_2026','0.0003553'))
SEBI_RATE=float(os.getenv('SEBI_RATE','0.000001'))
STAMP_BUY_RATE=float(os.getenv('STAMP_BUY_RATE','0.00003'))
STT_SELL_RATE=float(os.getenv('STT_SELL_RATE','0.001'))
STT_SELL_RATE_2026=float(os.getenv('STT_SELL_RATE_2026','0.0015'))
GST_RATE=float(os.getenv('GST_RATE','0.18'))
START=pd.Timestamp(os.getenv('START_DATE','2025-01-01')).date()
END=pd.Timestamp(os.getenv('END_DATE','2026-12-31')).date()
DATA=Path('data_cache'); DATA.mkdir(exist_ok=True)
OUT=Path(os.getenv('OUT_DIR','results')); OUT.mkdir(exist_ok=True)

def opt_file(y):
    return Path(hf_hub_download(repo_id='rissin/nse-options-intraday',
        filename=f'upstox_intraday/NIFTY/NIFTY_{y}.parquet',
        repo_type='dataset', token=os.getenv('HF_TOKEN'), cache_dir=str(DATA)))

def spot_files(y):
    if y==2026:
        names=['NIFTY50_1min_20260101_to_20260908.csv',
               'NIFTY50_1min_20260901_to_20260930.csv']
    else:
        names=[f'NIFTY50_1min_{y}.csv']
    out=[]
    for name in names:
        p=DATA/name
        if not p.exists():
            urllib.request.urlretrieve(
                f'https://raw.githubusercontent.com/technovusin/nifty50-historical-data/main/1min/{y}/{name}',p)
        out.append(p)
    return out

def load_spot(y):
    frames=[pd.read_csv(p,usecols=['Timestamp','Open','High','Low','Close']) for p in spot_files(y)]
    s=pd.concat(frames,ignore_index=True).drop_duplicates(subset=['Timestamp'])
    s['timestamp']=pd.to_datetime(s['Timestamp'])
    s=s.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
    return s[['timestamp','open','high','low','close']].sort_values('timestamp')

def load_option_window(path, ex, start, end, strikes):
    filters=[('granularity','=','1min'),('expiry','=',str(ex)),
             ('timestamp','>=',pd.Timestamp(start).tz_localize('Asia/Kolkata')),
             ('timestamp','<=',pd.Timestamp(end).tz_localize('Asia/Kolkata')),
             ('strike','in',[float(x) for x in sorted(set(strikes))])]
    table=pq.read_table(path,columns=['timestamp','expiry','strike','option_type','open','high','low','close'],
                        filters=filters,use_threads=True,pre_buffer=True)
    df=table.to_pandas()
    if df.empty: return df
    df['timestamp']=pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    df['expiry']=pd.to_datetime(df['expiry']).dt.date
    return df.sort_values('timestamp')

def atm(spot):
    return int(math.floor(float(spot)/50+0.5)*50)

def strike(spot,side,n):
    a=atm(spot)
    return a+n*50 if side=='CE' else a-n*50

def lot_size(ex):
    return 75 if pd.Timestamp(ex).date() <= pd.Timestamp('2025-12-30').date() else 65

def exec_px(open_px,action):
    if action in ('BUY','BUYBACK'):
        return max(0.05,float(open_px)+SLIP)
    return max(0.05,float(open_px)-SLIP)

def order_cost(price, action, lot, trade_date=None):
    turnover=float(price)*lot
    td=pd.Timestamp(trade_date).date() if trade_date is not None else None
    exchange_rate=EXCHANGE_RATE_2026 if td is not None and td>=pd.Timestamp('2026-03-01').date() else EXCHANGE_RATE
    stt_rate=STT_SELL_RATE_2026 if td is not None and td>=pd.Timestamp('2026-04-01').date() else STT_SELL_RATE
    brokerage=BROKER
    exchange=turnover*exchange_rate
    sebi=turnover*SEBI_RATE
    stamp=turnover*STAMP_BUY_RATE if action in ('BUY','BUYBACK') else 0.0
    stt=turnover*stt_rate if action=='SELL' else 0.0
    gst=GST_RATE*(brokerage+exchange+sebi)
    return brokerage+exchange+sebi+stamp+stt+gst

def position_mtm(cash,signed,opt_idx,ts,lot):
    mtm=0.0
    for (k,typ),q in signed.items():
        r=opt_idx.get((ts,float(k),typ))
        if r is None: return None
        mtm += q*float(r[3])*lot
    return cash+mtm

def close_position(cash,signed,opt_idx,ts,lot):
    fees=0.0
    orders=0
    for (k,typ),q in list(signed.items()):
        r=opt_idx.get((ts,float(k),typ))
        if r is None: return None,None,'missing_expiry_leg'
        action='SELL' if q>0 else 'BUYBACK'
        px=exec_px(r[0],action)
        cash += q*px*lot
        fees += order_cost(px,action,lot,ts)
        orders += 1
    return cash,fees,orders

def run_trade(opt_idx,ss,ex,side):
    t0=pd.Timestamp(ss.iloc[0].timestamp).replace(hour=10,minute=0)
    end=pd.Timestamp(ex).replace(hour=15,minute=29)
    ss=ss[(ss.timestamp>=t0)&(ss.timestamp<=end)].reset_index(drop=True)
    if ss.empty: return None,'no_spot'
    s0=float(ss.iloc[0].close)
    lot=lot_size(ex)
    k6,k7,k8=[strike(s0,side,n) for n in (6,7,8)]
    signed={}; cash=0.0; fees=0.0; orders=0
    for k,q in [(k6,1),(k7,-1),(k8,-1)]:
        r=opt_idx.get((t0,float(k),side))
        if r is None or pd.isna(r[0]) or float(r[0])<=0:
            return None,'missing_entry_leg'
        action='BUY' if q>0 else 'SELL'
        px=exec_px(r[0],action)
        cash += -q*px*lot
        fees += order_cost(px,action,lot,t0)
        orders += 1
        signed[(float(k),side)]=q

    roll_done=False
    roll_ts=None
    peak=-1e18
    trough=1e18
    trigger=k8

    for i,row in enumerate(ss.itertuples(index=False)):
        ts=row.timestamp
        pnl=position_mtm(cash,signed,opt_idx,ts,lot)
        if pnl is not None:
            peak=max(peak,pnl); trough=min(trough,pnl)

        if not roll_done and ts>=t0 and ts<end:
            breach=(float(row.high)>trigger) if side=='CE' else (float(row.low)<trigger)
            if breach and i+1<len(ss):
                nts=ss.iloc[i+1].timestamp
                old=opt_idx.get((nts,float(k8),side))
                opp='PE' if side=='CE' else 'CE'
                new=opt_idx.get((nts,float(k8),opp))
                if old is None: return None,'missing_roll_buyback'
                if new is None: return None,'missing_roll_opposite_sale'

                buy_px=exec_px(old[0],'BUYBACK')
                sell_px=exec_px(new[0],'SELL')
                cash += -buy_px*lot
                fees += order_cost(buy_px,'BUYBACK',lot,nts)
                orders += 1
                signed.pop((float(k8),side),None)

                cash += sell_px*lot
                fees += order_cost(sell_px,'SELL',lot,nts)
                orders += 1
                signed[(float(k8),opp)]=-1
                roll_done=True
                roll_ts=nts

    exit_ts=ss.iloc[-1].timestamp
    closed,exit_fees,exit_orders=close_position(cash,signed,opt_idx,exit_ts,lot)
    if closed is None: return None,'missing_expiry_leg'
    fees += exit_fees
    orders += exit_orders

    return {
        'strategy':'Strategy 2 - Call' if side=='CE' else 'Strategy 1 - Put',
        'side':side,'expiry':str(ex),'entry_date':str(ss.iloc[0].timestamp.date()),
        'lot_size':lot,'entry_spot':s0,'otm6':k6,'otm7':k7,'otm8_initial':k8,
        'roll_trigger':k8,'roll_done':roll_done,
        'roll_ts':str(roll_ts) if roll_ts is not None else '',
        'exit_ts':str(exit_ts),'rolls':1 if roll_done else 0,'orders':orders,
        'gross_pnl':closed,'fees_proxy':fees,'net_pnl':closed-fees,
        'peak_mtm':peak,'trough_mtm':trough,'exit_reason':'expiry'
    },None

def expiry_candidates(spot,year):
    dates=sorted(pd.Series(spot.timestamp.dt.date.unique()).tolist())
    date_set=set(dates)
    tues=pd.date_range(f'{year}-01-01',f'{year}-12-31',freq='W-TUE').date
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
        print(f'loading spot {y}',flush=True)
        spot=load_spot(y); path=opt_file(y)
        exps=[e for e in expiry_candidates(spot,y) if START<=e<=END]
        print(f'{y}: {len(exps)} candidate expiries',flush=True)
        for n,ex in enumerate(exps,1):
            entry=(pd.Timestamp(ex)-pd.Timedelta(days=4)).date()
            if spot[spot.timestamp.dt.date==entry].empty:
                skips.append([str(ex),'entry_not_trading_day']); continue
            window=spot[(spot.timestamp.dt.date>=entry)&(spot.timestamp.dt.date<=ex)].copy()
            if window.empty:
                skips.append([str(ex),'no_spot_window']); continue
            t0=pd.Timestamp(entry).replace(hour=10,minute=0)
            entry_rows=window[window.timestamp==t0]
            if entry_rows.empty:
                skips.append([str(ex),'no_10am_spot']); continue
            entry_spot=float(entry_rows.iloc[0].close)
            candidates=set()
            for side0 in ('CE','PE'):
                for nlev in (6,7,8):
                    candidates.add(strike(entry_spot,side0,nlev))
            start_ts=t0; end_ts=pd.Timestamp(ex).replace(hour=15,minute=29)
            od=load_option_window(path,ex,start_ts,end_ts,candidates)
            idx={(r.timestamp,float(r.strike),r.option_type):(r.open,r.high,r.low,r.close)
                 for r in od.itertuples(index=False)}
            for side in ('CE','PE'):
                r,e=run_trade(idx,window,ex,side)
                if r is not None: rows.append(r)
                else: skips.append([str(ex),side,e])
            if n%10==0: print(f'{y}: processed {n}/{len(exps)} expiries',flush=True)
        data_meta.append({'year':y,'spot_rows':len(spot),'expiry_candidates':len(exps)})

    res=pd.DataFrame(rows)
    res.to_csv(OUT/'strategy_v3_trades.csv',index=False)
    summary=(res.groupby(['strategy','side'])
        .agg(trades=('net_pnl','size'),
             win_rate=('net_pnl',lambda x:float((x>0).mean())),
             avg_net=('net_pnl','mean'),median_net=('net_pnl','median'),
             total_net=('net_pnl','sum'),gross_total=('gross_pnl','sum'),
             total_fees=('fees_proxy','sum'),avg_fees=('fees_proxy','mean'),
             roll_rate=('rolls','mean'),avg_orders=('orders','mean'),
             worst_trade=('net_pnl','min')).reset_index())
    summary.to_csv(OUT/'strategy_v3_summary.csv',index=False)
    quality={'years':YEARS,'trades':len(res),'skips':skips,'per_year':data_meta,
              'source':'rissin/nse-options-intraday + technovusin/nifty50-historical-data',
              'resolution':'1min','strategy_version':'V3 static OTM8 reversal',
              'trigger':'spot high > initial OTM8 for CE; spot low < initial OTM8 for PE',
              'roll':'buy original OTM8 and sell opposite option at same initial OTM8 strike; one roll maximum',
              'expiry_exit':'15:29 bar open','accounting':'cash-flow based realization'}
    (OUT/'strategy_v3_data_quality.json').write_text(json.dumps(quality,indent=2,default=str))
    print(summary.to_string(index=False))

if __name__=='__main__':
    main()
