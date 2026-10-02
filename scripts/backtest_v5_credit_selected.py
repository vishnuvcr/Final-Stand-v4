import json, math, os, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download, HfApi

YEARS=[int(x) for x in os.getenv('YEARS','2025,2026').split(',') if x.strip()]
START=pd.Timestamp(os.getenv('START_DATE','2025-01-01')).date()
END=pd.Timestamp(os.getenv('END_DATE','2026-09-30')).date()
SLIP=float(os.getenv('SLIPPAGE_POINTS','0.10'))
BROKER=float(os.getenv('BROKERAGE_PER_ORDER','10'))
TARGET_FRAC=float(os.getenv('TARGET_FRAC','0.90'))
STOP_MULT=float(os.getenv('STOP_MULT','0'))
HF_REVISION=os.getenv('HF_REVISION','main')
_RESOLVED_HF_REVISION=None
DATA=Path('data_cache'); DATA.mkdir(exist_ok=True)
OUT=Path(os.getenv('OUT_DIR','results')); OUT.mkdir(exist_ok=True)

EXCHANGE_PRE=0.0003503
EXCHANGE_POST=0.0003553
SEBI_RATE=0.000001
STAMP_BUY_RATE=0.00003
STT_PRE=0.001
STT_POST=0.0015
GST_RATE=0.18

def resolved_hf_revision():
    global _RESOLVED_HF_REVISION
    if _RESOLVED_HF_REVISION is not None:
        return _RESOLVED_HF_REVISION
    if HF_REVISION != 'main':
        _RESOLVED_HF_REVISION=HF_REVISION
    else:
        info=HfApi(token=os.getenv('HF_TOKEN')).dataset_info('rissin/nse-options-intraday')
        _RESOLVED_HF_REVISION=info.sha
    return _RESOLVED_HF_REVISION

def opt_file(y):
    rev=resolved_hf_revision()
    return Path(hf_hub_download(repo_id='rissin/nse-options-intraday', filename=f'upstox_intraday/NIFTY/NIFTY_{y}.parquet', repo_type='dataset', revision=rev, token=os.getenv('HF_TOKEN'), cache_dir=str(DATA/'hf')))

def spot_files(y):
    if y==2026:
        names=[f'NIFTY50_1min_2026-{m:02d}.csv' for m in range(1,10)]
    else:
        names=[f'NIFTY50_1min_{y}.csv']
    out=[]
    for name in names:
        p=DATA/name
        if not p.exists():
            url=f'https://raw.githubusercontent.com/technovusin/nifty50-historical-data/main/1min/{y}/{name}'
            urllib.request.urlretrieve(url,p)
        out.append(p)
    return out

def load_spot(y):
    frames=[]
    for p in spot_files(y):
        frames.append(pd.read_csv(p,usecols=['Timestamp','Open','High','Low','Close']))
    s=pd.concat(frames,ignore_index=True).drop_duplicates(subset=['Timestamp'])
    s['timestamp']=pd.to_datetime(s['Timestamp'])
    s=s.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close'})
    return s[['timestamp','open','high','low','close']].sort_values('timestamp')

def atm(spot, step=50):
    return int(math.floor(float(spot)/step+0.5)*step)

def strikes_for_entry(spot):
    a=atm(spot)
    return {'ce6':a+300,'ce7':a+350,'ce8':a+400,'pe6':a-300,'pe7':a-350,'pe8':a-400}

def select_side(pe6,pe7,pe8,ce6,ce7,ce8):
    pc=float(pe7)+float(pe8)-float(pe6)
    cc=float(ce7)+float(ce8)-float(ce6)
    if cc>pc: return ('CALL',cc,False) if cc>0 else ('NONE',cc,False)
    if pc>cc: return ('PUT',pc,False) if pc>0 else ('NONE',pc,False)
    if pc>0: return ('PUT',pc,True)
    return ('NONE',pc,True)

def target_threshold(initial_net_credit_per_lot,target_frac):
    return float(initial_net_credit_per_lot)*float(target_frac)

def stop_threshold(initial_net_credit_per_lot,stop_mult):
    return -float(initial_net_credit_per_lot)*float(stop_mult)

def lot_size(ex):
    return 75 if pd.Timestamp(ex).date() <= pd.Timestamp('2025-12-30').date() else 65

def exec_px(open_px,action,slip=SLIP):
    if action in ('BUY','BUYBACK'): return max(0.05,float(open_px)+slip)
    return max(0.05,float(open_px)-slip)

def order_cost(price, action, qty, lot, trade_date, broker=BROKER):
    turnover=float(price)*abs(int(qty))*lot
    td=pd.Timestamp(trade_date).date()
    exchange_rate=EXCHANGE_POST if td>=pd.Timestamp('2026-03-01').date() else EXCHANGE_PRE
    stt_rate=STT_POST if td>=pd.Timestamp('2026-04-01').date() else STT_PRE
    exchange=turnover*exchange_rate
    sebi=turnover*SEBI_RATE
    stamp=turnover*STAMP_BUY_RATE if action in ('BUY','BUYBACK') else 0.0
    stt=turnover*stt_rate if action=='SELL' else 0.0
    gst=GST_RATE*(broker+exchange+sebi)
    return broker+exchange+sebi+stamp+stt+gst

def load_option_window(path, ex, start, end, strikes):
    filters=[('expiry','=',str(ex)),('timestamp','>=',pd.Timestamp(start).tz_localize('Asia/Kolkata')),('timestamp','<=',pd.Timestamp(end).tz_localize('Asia/Kolkata')),('strike','in',[float(x) for x in sorted(set(strikes))]),('granularity','=','1min')]
    t=pq.read_table(path,columns=['timestamp','expiry','strike','option_type','open','high','low','close'],filters=filters,use_threads=True,pre_buffer=True)
    df=t.to_pandas()
    if df.empty: return df
    df['timestamp']=pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    df['expiry']=pd.to_datetime(df['expiry']).dt.date
    return df.sort_values('timestamp')

def make_index(df):
    return {(r.timestamp,float(r.strike),str(r.option_type)):(r.open,r.high,r.low,r.close) for r in df.itertuples(index=False)}

def first_common_exit_time(idx, leg_keys, after_ts, expiry_ts=None):
    ts=set(t for (t,_,_) in idx.keys() if t>after_ts)
    if expiry_ts is not None: ts={t for t in ts if t<=expiry_ts}
    for t in sorted(ts):
        if all((t,float(k),typ) in idx and pd.notna(idx[(t,float(k),typ)][0]) and float(idx[(t,float(k),typ)][0])>0 for k,typ in leg_keys):
            return t
    return None

def mtm_net(cash,signed,idx,ts,lot,fees_paid):
    total=cash
    for (k,typ),q in signed.items():
        r=idx.get((ts,float(k),typ))
        if r is None or pd.isna(r[3]): return None
        total+=q*float(r[3])*lot
    return total-fees_paid

def close_position(cash,signed,idx,ts,lot,fees_paid,trade_date):
    if ts is None: return None,None,None,'no_common_exit'
    orders=[]; exit_fees=0.0; c=cash
    for (k,typ),q in list(signed.items()):
        r=idx.get((ts,float(k),typ))
        if r is None or pd.isna(r[0]) or float(r[0])<=0: return None,None,None,'missing_exit_leg'
        action='SELL' if q>0 else 'BUYBACK'
        px=exec_px(r[0],action)
        c += q*px*lot
        exit_fees += order_cost(px,action,abs(int(q)),lot,trade_date)
        orders.append({'strike':k,'option_type':typ,'qty':int(q),'action':action,'price':px})
    return c-fees_paid-exit_fees,exit_fees,orders,None

def discover_calendar(path,year):
    pf=pq.ParquetFile(path)
    expiries=set(); spot10={}
    for batch in pf.iter_batches(columns=['timestamp','expiry'],batch_size=1_000_000):
        x=batch.to_pandas()
        x['timestamp']=pd.to_datetime(x['timestamp']).dt.tz_localize(None)
        x['date']=x['timestamp'].dt.date
        x['expiry']=pd.to_datetime(x['expiry'],errors='coerce').dt.date
        expiries.update(x['expiry'].dropna().tolist())
    return sorted(d for d in expiries if START<=d<=END)

def backtest_candidate(ex,entry,spot):
    entry_ts=pd.Timestamp(entry).replace(hour=10,minute=0)
    expiry_ts=pd.Timestamp(ex).replace(hour=15,minute=29)
    entry_spot=float(spot.loc[spot.timestamp==entry_ts,'open'].iloc[0])
    ks=strikes_for_entry(entry_spot)
    path=opt_file(ex.year)
    window=load_option_window(path,ex,entry_ts,expiry_ts,list(ks.values()))
    if window.empty: return None,'no_option_rows'
    idx=make_index(window)
    vals={}
    for label,k in ks.items():
        typ='CE' if label.startswith('ce') else 'PE'
        r=idx.get((entry_ts,float(k),typ))
        vals[label]=None if r is None else float(r[0]) if pd.notna(r[0]) else None
    if any(v is None or v<=0 for v in vals.values()): return None,'missing_entry_leg'
    side,raw_credit,tie=select_side(vals['pe6'],vals['pe7'],vals['pe8'],vals['ce6'],vals['ce7'],vals['ce8'])
    if side=='NONE': return None,'no_positive_credit'
    lot=lot_size(ex)
    labels=['ce6','ce7','ce8'] if side=='CALL' else ['pe6','pe7','pe8']
    types=['CE','CE','CE'] if side=='CALL' else ['PE','PE','PE']
    qty=[1,-1,-1]
    legs=list(zip([ks[x] for x in labels],types,qty,labels))
    cash=0.0; entry_fees=0.0; signed={}
    for k,typ,q,label in legs:
        r=idx.get((entry_ts,float(k),typ))
        action='BUY' if q>0 else 'SELL'
        px=exec_px(r[0],action)
        cash += -q*px*lot
        entry_fees += order_cost(px,action,abs(q),lot,entry_ts)
        signed[(float(k),typ)]=q
    initial_net_credit_per_lot=raw_credit-3*SLIP
    target_rupees=target_threshold(initial_net_credit_per_lot*lot,TARGET_FRAC)
    stop_rupees=stop_threshold(initial_net_credit_per_lot*lot,STOP_MULT) if STOP_MULT>0 else None
    trigger=None; trigger_type=None; trigger_value=None; peak=-1e18; trough=1e18
    common_times=sorted({t for (t,_,_) in idx.keys() if entry_ts<=t<expiry_ts})
    for t in common_times:
        m=mtm_net(cash,signed,idx,t,lot,entry_fees)
        if m is None: continue
        peak=max(peak,m); trough=min(trough,m)
        if STOP_MULT>0 and m<=stop_rupees:
            trigger=t; trigger_type='stop'; trigger_value=m; break
        if m>=target_rupees:
            trigger=t; trigger_type='target'; trigger_value=m; break
    if trigger is not None:
        exit_ts=first_common_exit_time(idx,[(k,typ) for k,typ,_,_ in legs],trigger,expiry_ts)
        exit_reason=trigger_type
    else:
        exit_ts=expiry_ts if all((expiry_ts,float(k),typ) in idx and pd.notna(idx[(expiry_ts,float(k),typ)][0]) and float(idx[(expiry_ts,float(k),typ)][0])>0 for k,typ,_,_ in legs) else None
        exit_reason='expiry' if exit_ts is not None else 'missing_expiry_leg'
    net_pnl,exit_fees,orders,reason=close_position(cash,signed,idx,exit_ts,lot,entry_fees,exit_ts)
    if reason: return None,reason
    return {
        'expiry':str(ex),'entry_date':str(entry),'side':side,'selected_credit':raw_credit,'other_credit':(vals['ce7']+vals['ce8']-vals['ce6']) if side=='PUT' else (vals['pe7']+vals['pe8']-vals['pe6']),'selection_margin':abs((vals['ce7']+vals['ce8']-vals['ce6'])-(vals['pe7']+vals['pe8']-vals['pe6'])),'atm':atm(entry_spot),'entry_spot':entry_spot,'lot_size':lot,'target_fraction':TARGET_FRAC,'stop_multiple':STOP_MULT,'initial_net_credit_per_lot':initial_net_credit_per_lot,'target_rupees':target_rupees,'stop_rupees':stop_rupees if stop_rupees is not None else np.nan,'trigger_timestamp':str(trigger) if trigger is not None else '','exit_timestamp':str(exit_ts),'exit_reason':exit_reason,'trigger_pnl':trigger_value if trigger_value is not None else np.nan,'gross_pnl':float(net_pnl+entry_fees+exit_fees),'fees_proxy':float(entry_fees+exit_fees),'net_pnl':float(net_pnl),'peak_mtm':float(peak),'trough_mtm':float(trough),'runup_to_drawdown':float(peak-trough),'orders':len(orders)+3,'ce6':ks['ce6'],'ce7':ks['ce7'],'ce8':ks['ce8'],'pe6':ks['pe6'],'pe7':ks['pe7'],'pe8':ks['pe8']
    },None

def build_trade_rows():
    all_rows=[]; skips=[]; meta=[]
    for y in YEARS:
        spot=load_spot(y)
        dates=sorted(pd.Series(spot.timestamp.dt.date.unique()).tolist())
        ydates=set(dates)
        exps=[e for e in discover_calendar(opt_file(y),y) if e in ydates]
        exps_all=exps[:]
        for ex in exps:
            prev=[d for d in dates if d<ex]
            if len(prev)<4:
                skips.append([str(ex),'insufficient_prior_trading_days']); continue
            entry=prev[-4]
            if not (0 < (ex-entry).days <= 8):
                skips.append([str(ex),'not_weekly_near_expiry']); continue
            upcoming=[d for d in exps_all if d>=entry]
            if not upcoming or upcoming[0] != ex:
                skips.append([str(ex),'not_nearest_expiry_on_entry']); continue
            if entry<START or entry>END: continue
            if pd.Timestamp(entry).replace(hour=10,minute=0) not in set(spot.timestamp): skips.append([str(ex),'no_10am_spot']); continue
            r,reason=backtest_candidate(ex,entry,spot)
            if r is not None: all_rows.append(r)
            else: skips.append([str(ex),reason])
        meta.append({'year':y,'spot_rows':len(spot),'expiry_candidates':len(exps)})
    df=pd.DataFrame(all_rows).sort_values('expiry').reset_index(drop=True)
    return df,skips,meta

def main():
    rows,skips,meta=build_trade_rows()
    rows.to_csv(OUT/'strategy_v5_trades.csv',index=False)
    q={'strategy_version':'V5 credit-selected OTM6/7/8','target_fraction':TARGET_FRAC,'stop_multiple':STOP_MULT,'trades':len(rows),'skips':skips,'per_year':meta,'source':'rissin/nse-options-intraday@'+resolved_hf_revision()+' + technovusin/nifty50-historical-data','entry':'4 trading sessions before actual expiry at 10:00 IST','execution':'10:00 option-bar open; trigger on close; exit first common next open; otherwise 15:29 expiry open','cost_model':'Paytm Money + NSE/SEBI/STT/stamp/GST + slippage','positive_credit_filter':True}
    (OUT/'strategy_v5_data_quality.json').write_text(json.dumps(q,indent=2,default=str))
    print(json.dumps({'trades':len(rows),'skips':len(skips)},indent=2))

if __name__=='__main__': main()