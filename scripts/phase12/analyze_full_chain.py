#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import binomtest
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,balanced_accuracy_score,matthews_corrcoef,roc_auc_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
E=Path("results/phase12_full_chain_features.csv");J=Path("results/phase12_full_chain_analysis.json");M=Path("results/phase12_full_chain_analysis.md")
def metrics(y,p,prob=None):
 yb=(np.asarray(y)=="bullish").astype(int);pb=(np.asarray(p)=="bullish").astype(int);n=len(yb);correct=int((yb==pb).sum())
 d={"n":n,"correct":correct,"accuracy":float(accuracy_score(yb,pb)),"balanced_accuracy":float(balanced_accuracy_score(yb,pb)),"mcc":float(matthews_corrcoef(yb,pb)),"exact_binomial_p_50":float(binomtest(correct,n,.5).pvalue) if n else None}
 if prob is not None and len(np.unique(yb))==2:d["roc_auc"]=float(roc_auc_score(yb,prob))
 return d
def groups(df):
 cols=[c for c in df if c not in {"expiry_date","observation_timestamp_ist","realized_direction","expiry_return"}]
 return {"aggregate":[c for c in cols if "_d" not in c],"surface":[c for c in cols if "_d" in c],"oi_only":[c for c in cols if "oi" in c.lower()],"volume_only":[c for c in cols if "volume" in c.lower()],"premium_only":[c for c in cols if "open" in c.lower() or "premium" in c.lower()],"all":cols}
def cv(dev,cols,C,y):
 x=dev[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan);s=TimeSeriesSplit(5);sc=[]
 for tr,va in s.split(x):
  med=x.iloc[tr].median();xt=x.iloc[tr].fillna(med);xv=x.iloc[va].fillna(med);m=Pipeline([("scale",StandardScaler()),("logit",LogisticRegression(max_iter=4000,solver="liblinear",penalty="l1",C=C))]);m.fit(xt,y.iloc[tr]);sc.append(balanced_accuracy_score(y.iloc[va],m.predict(xv)))
 return float(np.mean(sc))
def bootstrap_accuracy(y,p,B=2000,seed=12345):
 rng=np.random.default_rng(seed);yb=(np.asarray(y)=="bullish").astype(int);pb=(np.asarray(p)=="bullish").astype(int)
 if len(yb)==0:return [None,None]
 vals=[]
 for _ in range(B):
  idx=rng.integers(0,len(yb),len(yb));vals.append(float((yb[idx]==pb[idx]).mean()))
 return [float(np.quantile(vals,.025)),float(np.quantile(vals,.975))]

def tree_holdout(train,test,cols,depth):
 xt=train[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan);xv=test[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan)
 med=xt.median();xt=xt.fillna(med);xv=xv.fillna(med);y=(train.realized_direction=="bullish").astype(int)
 m=DecisionTreeClassifier(max_depth=depth,min_samples_leaf=8,random_state=12345,class_weight="balanced");m.fit(xt,y);pr=m.predict_proba(xv)[:,1]
 return metrics(test.realized_direction,np.where(pr>=.5,"bullish","bearish"),pr)

def fit(train,test,cols,C):
 xt=train[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan);xv=test[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan);med=xt.median();xt=xt.fillna(med);xv=xv.fillna(med);y=(train.realized_direction=="bullish").astype(int)
 m=Pipeline([("scale",StandardScaler()),("logit",LogisticRegression(max_iter=5000,solver="liblinear",penalty="l1",C=C))]);m.fit(xt,y);pr=m.predict_proba(xv)[:,1];return metrics(test.realized_direction,np.where(pr>=.5,"bullish","bearish"),pr)
def main():
 d=pd.read_csv(E);d.expiry_date=pd.to_datetime(d.expiry_date);d=d.sort_values("expiry_date").reset_index(drop=True);dev=d[d.expiry_date<pd.Timestamp("2026-01-01")].reset_index(drop=True);hold=d[d.expiry_date>=pd.Timestamp("2026-01-01")].reset_index(drop=True);g=groups(dev);y=(dev.realized_direction=="bullish").astype(int);cand=[]
 for fam,cols in g.items():
  if not cols:continue
  for C in [.01,.03,.1,.3,1.0]:cand.append({"family":fam,"C":C,"cv_balanced_accuracy":cv(dev,cols,C,y),"n_features":len(cols)})
 cand.sort(key=lambda z:(-z["cv_balanced_accuracy"],z["n_features"],z["family"]));best=cand[0];holdm=fit(dev,hold,g[best["family"]],best["C"])
 # Refit the frozen development model to obtain holdout predictions for the bootstrap interval.
 xt=dev[g[best["family"]]].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan);xv=hold[g[best["family"]]].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan);med=xt.median();xt=xt.fillna(med);xv=xv.fillna(med);yy=(dev.realized_direction=="bullish").astype(int);mm=Pipeline([("scale",StandardScaler()),("logit",LogisticRegression(max_iter=5000,solver="liblinear",penalty="l1",C=best["C"]))]);mm.fit(xt,yy);ppred=np.where(mm.predict_proba(xv)[:,1]>=.5,"bullish","bearish");holdm["accuracy_bootstrap_95ci"]=bootstrap_accuracy(hold.realized_direction,ppred)
 holdm["tree_depth2"]=tree_holdout(dev,hold,g[best["family"]],2)
 rng=np.random.default_rng(12345);obs=best["cv_balanced_accuracy"];perm=[]
 for _ in range(500):
  yp=pd.Series(rng.permutation(y.to_numpy()));mx=-np.inf
  for fam,cols in g.items():
   if not cols:continue
   for C in [.01,.1,1.0]:mx=max(mx,cv(dev,cols,C,yp))
  perm.append(mx)
 pp=(1+sum(x>=obs for x in perm))/(1+len(perm))
 res={"protocol":{"all_available_strikes":True,"surface_grid":"ATM-relative -30..+30","development":"before 2026-01-01","holdout":"2026 onward","cv":"5-fold chronological","permutations":500},"coverage":{"development":len(dev),"holdout":len(hold),"median_strikes":float(d.available_strikes.median()),"min_strikes":int(d.available_strikes.min()),"max_strikes":int(d.available_strikes.max())},"selected_model":best,"holdout":holdm,"multiple_testing_permutation_p":float(pp),"top_screen":cand[:20]}
 J.write_text(json.dumps(res,indent=2)+"\n");lines=["# Phase 12 Full-Chain Analysis","",f"Development {len(dev)} events; 2026 holdout {len(hold)} events.",f"Available strikes/event: median {d.available_strikes.median():.0f}, range {d.available_strikes.min()}–{d.available_strikes.max()}.","", "## Selected model",json.dumps(best,indent=2),"","## 2026 holdout",json.dumps(holdm,indent=2), "",f"## Multiple-testing permutation p={pp:.4f}","","This is a full-chain screen. No trading translation is authorized without independent replication and robustness."]
 lines+=["","## Top screens","| Family | C | CV balanced accuracy | Features |","|---|---:|---:|---:|"]+[f"| {r['family']} | {r['C']} | {r['cv_balanced_accuracy']:.3f} | {r['n_features']} |" for r in cand[:10]]
 M.write_text("\n".join(lines)+"\n")
if __name__=="__main__":main()
