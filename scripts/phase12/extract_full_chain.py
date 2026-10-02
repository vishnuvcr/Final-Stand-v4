#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np,pandas as pd
IST="Asia/Kolkata"
def norm_ts(s):
 ts=pd.to_datetime(s,errors="coerce")
 return ts.dt.tz_localize(IST) if ts.dt.tz is None else ts.dt.tz_convert(IST)
def num(df,names):
 for n in names:
  if n in df.columns:return pd.to_numeric(df[n],errors="coerce")
 return pd.Series(np.nan,index=df.index)
def features(e,chain):
 o={"expiry_date":str(e.expiry_date.date()),"observation_timestamp_ist":str(e.observation_timestamp_ist),"realized_direction":e.realized_direction,"expiry_return":float(e.expiry_return)}
 if chain.empty:o.update({"available_strikes":0,"available_contracts":0});return o
 c=chain.copy();c["strike"]=pd.to_numeric(c["strike"],errors="coerce");c["open"]=num(c,["open","ltp"]);c["oi"]=num(c,["open_interest","oi"]);c["volume"]=num(c,["volume"]);c["option_type"]=c["option_type"].astype(str).str.upper();c=c.dropna(subset=["strike","option_type"])
 interval=float(e.strike_interval);atm=float(e.atm_strike);c["dist"]=np.round((c.strike-atm)/interval).astype(int);c=c.drop_duplicates(["strike","option_type"],keep="last")
 o["available_strikes"]=int(c.strike.nunique());o["available_contracts"]=int(len(c))
 for typ,p in [("CE","ce"),("PE","pe")]:
  g=c[c.option_type==typ].copy()
  for m in ["open","oi","volume"]:
   v=pd.to_numeric(g[m],errors="coerce");o[f"{p}_{m}_sum"]=float(v.sum(min_count=1)) if v.notna().any() else np.nan
   o[f"{p}_{m}_count"]=int(v.notna().sum())
  for m in ["oi","volume","open"]:
   v=pd.to_numeric(g[m],errors="coerce");w=v.clip(lower=0);den=float(w.sum()) if w.notna().any() else 0
   if den:
    wd=float((g.dist*w).sum()/den);o[f"{p}_{m}_weighted_dist"]=wd;o[f"{p}_{m}_dist_sd"]=float(np.sqrt(((g.dist-wd)**2*w).sum()/den));idx=w.idxmax();o[f"{p}_{m}_wall_dist"]=int(g.loc[idx,"dist"]);o[f"{p}_{m}_wall_share"]=float(w.max()/den)
   else:o[f"{p}_{m}_weighted_dist"]=np.nan;o[f"{p}_{m}_dist_sd"]=np.nan;o[f"{p}_{m}_wall_dist"]=np.nan;o[f"{p}_{m}_wall_share"]=np.nan
 for name,a,b in [("oi",o.get("ce_oi_sum",np.nan),o.get("pe_oi_sum",np.nan)),("volume",o.get("ce_volume_sum",np.nan),o.get("pe_volume_sum",np.nan)),("premium",o.get("ce_open_sum",np.nan),o.get("pe_open_sum",np.nan))]:
  o[f"{name}_pcr"]=float(b/a) if np.isfinite(a) and a else np.nan;den=a+b;o[f"{name}_imbalance"]=float((b-a)/den) if np.isfinite(den) and den else np.nan
 for d in range(-30,31):
  for typ,p in [("CE","ce"),("PE","pe")]:
   g=c[(c.option_type==typ)&(c.dist==d)]
   for m in ["open","oi","volume"]:o[f"{p}_{m}_d{d:+d}"]=float(g.iloc[0][m]) if len(g) and pd.notna(g.iloc[0][m]) else np.nan
 return o
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--events",default="results/phase11_events.csv");ap.add_argument("--options-dir",default="data_cache/phase11/options_primary");ap.add_argument("--output",default="results/phase12_full_chain_features.csv");ap.add_argument("--manifest",default="results/phase12_full_chain_manifest.json");a=ap.parse_args()
 e=pd.read_csv(a.events);e.expiry_date=pd.to_datetime(e.expiry_date);e.observation_timestamp_ist=norm_ts(e.observation_timestamp_ist);root=Path(a.options_dir);rows=[];audit=[]
 for _,ev in e.sort_values("expiry_date").iterrows():
  ex=ev.expiry_date.strftime("%Y-%m-%d");files=sorted(root.glob(f"*{ex}*.parquet"));frames=[]
  for f in files:
   try:d=pd.read_parquet(f)
   except Exception as exc:audit.append({"expiry":ex,"error":repr(exc)});continue
   if "timestamp" not in d.columns:continue
   d.timestamp=norm_ts(d.timestamp);d=d[d.timestamp==ev.observation_timestamp_ist]
   if len(d):frames.append(d)
  chain=pd.concat(frames,ignore_index=True) if frames else pd.DataFrame();rows.append(features(ev,chain));audit.append({"expiry":ex,"files":len(files),"rows":len(chain)})
 out=pd.DataFrame(rows);out.to_csv(a.output,index=False);Path(a.manifest).write_text(json.dumps({"events":len(e),"extracted":len(out),"nonempty":int((out.available_contracts>0).sum()),"audit":audit,"no_interpolation":True},indent=2)+"\n")
if __name__=="__main__":main()
