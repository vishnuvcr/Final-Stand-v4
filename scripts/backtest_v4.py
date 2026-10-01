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
    return Path(hf_hub_download(
        repo_id='rissin/nse-options-intraday',
        filename=f'upstox_intraday/NIFTY/NIFTY_{y}.parquet',
        repo_type='dataset', token=os.getenv('HF_TOKEN'), cache_dir=str(DATA)
    ))

def spot_files(y):
    if y==2026:
        names=[f'NIFTY50_1min_2026-{m:02d}.csv' for m in range(1,11)]
    else:
        names=[f'NIFTY50_1min_{y}.csv']
    out=[]
    for name in names:
        p=DATA/name
        if not p.exists():
            urllib.request.urlretrieve(
                f'https://raw.githubusercontent.com/technovusin/nifty50-historical-data/main/1min/{y}/{name}', p)
        out.append(p)
    return out

def load_spot(y):
    frames=[pd.read_csv(p, usecols=['Timestamp','Open','High','Low','Close']) for p in spot_files(y)]
    s=pd.concat(frames, ignore_index=True).drop_duplicates(subset=['Timestamp'])
    s['timestamp']=pd.to_datetime(s['Timestamp'])
    s=s.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
    return s[['timestamp','open','high','low','close']].sort_values('timestamp')

def load_option_window(path, ex, start, end, strikes):
    filters=[
        ('granularity','=','1min'),
        ('expiry','=',str(ex)),
        ('timestamp','>=',pd.Timestamp(start).tz_localize('Asia/Kolkata')),
        ('timestamp','<=',pd.Timestamp(end).tz_localize('Asia/Kolkata')),
        ('strike','in',[float(x) for x in sorted(set(strikes))])
    ]
    table=pq.read_table(
        path,
        columns=['timestamp','expiry','strike','option_type','open','high','low','close'],
        filters=filters, use_threads=True, pre_buffer=True
    )
    df=table.to_pandas()
    if df.empty:
        return df
    df['timestamp']=pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    df['expiry']=pd.to_datetime(df['expiry']).dt.date
    return df.sort_values('timestamp')

def atm(spot, strike_step=50):
    return int(math.floor(float(spot)/strike_step+0.5)*strike_step)

def strikes_for_entry(spot):
    a=atm(spot)
    return {
        'ce16':a+16*50, 'ce17':a+17*50,
        'pe16':a-16*50, 'pe17':a-17*50
    }

def lot_size(ex):
    return 75 if pd.Timestamp(ex).date() <= pd.Timestamp('2025-12-30').date() else 65

def exec_px(open_px, action):
    return max(0.05, float(open_px)+(SLIP if action in ('BUY','BUYBACK') else -SLIP))

def order_cost(price, action, qty, lot, trade_date):
    turnover=float(price)*abs(int(qty))*lot
    td=pd.Timestamp(trade_date).date()
    exchange_rate=EXCHANGE_RATE_2026 if td>=pd.Timestamp('2026-03-01').date() else EXCHANGE_RATE
    stt_rate=STT_SELL_RATE_2026 if td>=pd.Timestamp('2026-04-01').date() else STT_SELL_RATE
    exchange=turnover*exchange_rate
    sebi=turnover*SEBI_RATE
    stamp=turnover*STAMP_BUY_RATE if action in ('BUY','BUYBACK') else 0.0
    stt=turnover*stt_rate if action=='SELL' else 0.0
    gst=GST_RATE*(BROKER+exchange+sebi)
    return BROKER+exchange+sebi+stamp+stt+gst

def position_mtm(cash, signed, opt_idx, ts, lot):
    mtm=0.0
    for (k,typ),q in signed.items():
        r=opt_idx.get((ts,float(k),typ))
        if r is None:
            return None
        mtm += q*float(r[3])*lot
    return cash+mtm

def close_all(cash, signed, opt_idx, ts, lot):
    fees=0.0
    orders=0
    for (k,typ),q in list(signed.items()):
        r=opt_idx.get((ts,float(k),typ))
        if r is None:
            return None,None,None,None,'missing_expiry_leg'
        action='SELL' if q>0 else 'BUYBACK'
        qty=abs(int(q))
        px=exec_px(r[0], action)
        cash += q*px*lot
        fees += order_cost(px, action, qty, lot, ts)
        orders += 1
    return cash, fees, orders, ts, None

def run_trade(opt_idx, spot_window, expiry):
    entry_date=spot_window.iloc[0].timestamp.date()
    t0=pd.Timestamp(entry_date).replace(hour=10, minute=0)
    exit_ts=pd.Timestamp(expiry).replace(hour=15, minute=29)
    sw=spot_window[(spot_window.timestamp>=t0)&(spot_window.timestamp<=exit_ts)].reset_index(drop=True)
    if sw.empty:
        return None,'no_spot_window'
    er=sw[sw.timestamp==t0]
    if er.empty:
        return None,'no_10am_spot'
    entry_spot=float(er.iloc[0].open)
    ks=strikes_for_entry(entry_spot)
    lot=lot_size(expiry)
    legs=[
        (ks['ce16'],'CE',+1),
        (ks['ce17'],'CE',-2),
        (ks['pe16'],'PE',+1),
        (ks['pe17'],'PE',-2)
    ]
    signed={}
    cash=0.0
    fees=0.0
    orders=0
    entry_cashflow=0.0

    for k,typ,q in legs:
        r=opt_idx.get((t0,float(k),typ))
        if r is None or pd.isna(r[0]) or float(r[0])<=0:
            return None,'missing_entry_leg'
        action='BUY' if q>0 else 'SELL'
        px=exec_px(r[0],action)
        cash += -q*px*lot
        entry_cashflow += -q*px*lot
        fees += order_cost(px,action,abs(q),lot,t0)
        orders += 1
        signed[(float(k),typ)]=q

    peak=-1e18
    trough=1e18
    for row in sw.itertuples(index=False):
        pnl=position_mtm(cash,signed,opt_idx,row.timestamp,lot)
        if pnl is not None:
            peak=max(peak,pnl)
            trough=min(trough,pnl)

    closed,exit_fees,exit_orders,_,reason=close_all(cash,signed,opt_idx,exit_ts,lot)
    if closed is None:
        return None,reason or 'missing_expiry_leg'
    fees += exit_fees
    orders += exit_orders
    gross_pnl=float(closed)
    net_pnl=float(gross_pnl-fees)

    return {
        'strategy':'NIFTY OTM16/17 Double-Sided',
        'expiry':str(expiry),
        'entry_date':str(entry_date),
        'lot_size':lot,
        'entry_spot':entry_spot,
        'ce16':ks['ce16'],'ce17':ks['ce17'],'pe16':ks['pe16'],'pe17':ks['pe17'],
        'entry_cashflow':entry_cashflow,
        'gross_pnl':gross_pnl,'fees_proxy':fees,'net_pnl':net_pnl,
        'peak_mtm':peak,'trough_mtm':trough,
        'orders':orders,'exit_ts':str(exit_ts),'exit_reason':'expiry'
    },None

def expiry_candidates(spot,year):
    dates=sorted(pd.Series(spot.timestamp.dt.date.unique()).tolist())
    date_set=set(dates)
    tues=pd.date_range(f'{year}-01-01',f'{year}-12-31',freq='W-TUE').date
    out=[]
    for t in tues:
        if t in date_set:
            out.append(t)
        else:
            prev=[d for d in dates if d<t]
            if prev:
                out.append(prev[-1])
    return sorted(set(out))

def main():
    rows=[]
    skips=[]
    data_meta=[]
    for y in YEARS:
        print(f'loading spot {y}', flush=True)
        spot=load_spot(y)
        path=opt_file(y)
        exps=[e for e in expiry_candidates(spot,y) if START<=e<=END]
        print(f'{y}: {len(exps)} candidate expiries', flush=True)
        trading_dates=sorted(pd.Series(spot.timestamp.dt.date.unique()).tolist())
        for n,ex in enumerate(exps,1):
            prev=[d for d in trading_dates if d<ex]
            if len(prev)<4:
                skips.append([str(ex),'insufficient_prior_trading_days'])
                continue
            entry=prev[-4]
            entry_rows=spot[(spot.timestamp.dt.date==entry)&(spot.timestamp.dt.hour==10)&(spot.timestamp.dt.minute==0)]
            if entry_rows.empty:
                skips.append([str(ex),'no_10am_spot'])
                continue
            t0=pd.Timestamp(entry).replace(hour=10,minute=0)
            exit_ts=pd.Timestamp(ex).replace(hour=15,minute=29)
            window=spot[(spot.timestamp>=t0)&(spot.timestamp<=exit_ts)].copy()
            if window.empty:
                skips.append([str(ex),'no_spot_window'])
                continue
            entry_spot=float(entry_rows.iloc[0].open)
            ks=strikes_for_entry(entry_spot)
            candidates=list(ks.values())
            od=load_option_window(path,ex,t0,exit_ts,candidates)
            idx={(r.timestamp,float(r.strike),r.option_type):(r.open,r.high,r.low,r.close)
                 for r in od.itertuples(index=False)}
            r,e=run_trade(idx,window,ex)
            if r is not None:
                rows.append(r)
            else:
                skips.append([str(ex),e])
            if n%10==0:
                print(f'{y}: processed {n}/{len(exps)} expiries', flush=True)

        data_meta.append({'year':y,'spot_rows':len(spot),'expiry_candidates':len(exps)})

    res=pd.DataFrame(rows)
    res.to_csv(OUT/'strategy_v4_trades.csv',index=False)
    quality={
        'years':YEARS,
        'trades':len(res),
        'skips':skips,
        'per_year':data_meta,
        'source':'rissin/nse-options-intraday + technovusin/nifty50-historical-data',
        'resolution':'1min',
        'strategy_version':'V4 double-sided OTM16/17',
        'legs':['+1 CE16','-2 CE17','+1 PE16','-2 PE17'],
        'entry_rule':'4 trading days before expiry at 10:00 IST; 10:00 spot open selects strikes; 10:00 option open executes',
        'expiry_exit':'15:29 option bar open',
        'accounting':'cash-flow based realization',
        'slippage_points':SLIP,
        'brokerage_per_order':BROKER
    }
    (OUT/'strategy_v4_data_quality.json').write_text(json.dumps(quality,indent=2,default=str))
    print(f'Trades produced: {len(res)}', flush=True)

if __name__=='__main__':
    main()
