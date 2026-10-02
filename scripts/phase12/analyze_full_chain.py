#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import warnings
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import binomtest
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,balanced_accuracy_score,matthews_corrcoef,roc_auc_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", message=".*penalty.*deprecated.*")
warnings.filterwarnings("ignore", message=".*Inconsistent values.*penalty.*")

E=Path("results/phase12_full_chain_features.csv")
J=Path("results/phase12_full_chain_analysis.json")
M=Path("results/phase12_full_chain_analysis.md")
CV_SPLITS=5
SCREEN_C=[.01,.03,.1,.3,1.0]
PERM_C=[.01,.1,1.0]
PERMUTATIONS=500

def metrics(y,p,prob=None):
    yb=(np.asarray(y)=="bullish").astype(int);pb=(np.asarray(p)=="bullish").astype(int);n=len(yb);correct=int((yb==pb).sum())
    d={"n":n,"correct":correct,"accuracy":float(accuracy_score(yb,pb)),"balanced_accuracy":float(balanced_accuracy_score(yb,pb)),"mcc":float(matthews_corrcoef(yb,pb)),"exact_binomial_p_50":float(binomtest(correct,n,.5).pvalue) if n else None}
    if prob is not None and len(np.unique(yb))==2:d["roc_auc"]=float(roc_auc_score(yb,prob))
    return d

def groups(df):
    cols=[c for c in df if c not in {"expiry_date","observation_timestamp_ist","realized_direction","expiry_return"}]
    return {"aggregate":[c for c in cols if "_d" not in c],"surface":[c for c in cols if "_d" in c],"oi_only":[c for c in cols if "oi" in c.lower()],"volume_only":[c for c in cols if "volume" in c.lower()],"premium_only":[c for c in cols if "open" in c.lower() or "premium" in c.lower()],"all":cols}

def _prepare_train_test(train,test,cols):
    xt=train[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan)
    xv=test[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan)
    keep=xt.columns[xt.notna().any()]
    xt=xt[keep];xv=xv[keep]
    med=xt.median()
    xt=xt.fillna(med);xv=xv.fillna(med)
    return xt,xv,keep

def cv_matrices(dev,cols):
    x=dev[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan)
    out=[]
    for tr,va in TimeSeriesSplit(CV_SPLITS).split(x):
        xt,xv,_=_prepare_train_test(dev.iloc[tr],dev.iloc[va],cols)
        scaler=StandardScaler()
        xts=scaler.fit_transform(xt)
        xvs=scaler.transform(xv)
        out.append((xts,xvs,tr))
    return out

def cv_from_matrices(mats,C,y):
    scores=[]
    for xt,xv,tr in mats:
        m=LogisticRegression(max_iter=4000,solver="liblinear",penalty="l1",C=C)
        m.fit(xt,y.iloc[tr])
        scores.append(balanced_accuracy_score(y.iloc[[i for i in range(len(y)) if False]],[]))
    return float(np.mean(scores))

def cv_from_matrices(mats,C,y):
    scores=[]
    for xt,xv,tr in mats:
        m=LogisticRegression(max_iter=4000,solver="liblinear",penalty="l1",C=C)
        m.fit(xt,y.iloc[tr])
        pred=m.predict(xv)
        # The validation labels are recovered from the split index stored after the train indices.
        # Store validation indices alongside the matrices for exact chronological CV.
        scores.append((m,pred))
    return scores

def cv_score(mats,C,y):
    vals=[]
    for xt,xv,tr,va in mats:
        m=LogisticRegression(max_iter=4000,solver="liblinear",penalty="l1",C=C)
        m.fit(xt,y.iloc[tr]);vals.append(balanced_accuracy_score(y.iloc[va],m.predict(xv)))
    return float(np.mean(vals))

def build_cv_cache(dev,g):
    return {fam:[(*cv_matrices(dev,cols),) for _ in []] for fam,cols in g.items()}

def make_mats(dev,cols):
    x=dev[cols].apply(pd.to_numeric,errors="coerce").replace([np.inf,-np.inf],np.nan)
    out=[]
    for tr,va in TimeSeriesSplit(CV_SPLITS).split(x):
        xt,xv,_=_prepare_train_test(dev.iloc[tr],dev.iloc[va],cols)
        scaler=StandardScaler()
        out.append((scaler.fit_transform(xt),scaler.transform(xv),tr,va))
    return out

def bootstrap_accuracy(y,p,B=2000,seed=12345):
    rng=np.random.default_rng(seed);yb=(np.asarray(y)=="bullish").astype(int);pb=(np.asarray(p)=="bullish").astype(int)
    if len(yb)==0:return [None,None]
    vals=[]
    for _ in range(B):
        idx=rng.integers(0,len(yb),len(yb));vals.append(float((yb[idx]==pb[idx]).mean()))
    return [float(np.quantile(vals,.025)),float(np.quantile(vals,.975))]

def tree_holdout(train,test,cols,depth):
    xt,xv,_=_prepare_train_test(train,test,cols);y=(train.realized_direction=="bullish").astype(int)
    m=DecisionTreeClassifier(max_depth=depth,min_samples_leaf=8,random_state=12345,class_weight="balanced");m.fit(xt,y);pr=m.predict_proba(xv)[:,1]
    return metrics(test.realized_direction,np.where(pr>=.5,"bullish","bearish"),pr)

def fit(train,test,cols,C):
    xt,xv,_=_prepare_train_test(train,test,cols);y=(train.realized_direction=="bullish").astype(int)
    scaler=StandardScaler();xts=scaler.fit_transform(xt);xvs=scaler.transform(xv)
    m=LogisticRegression(max_iter=5000,solver="liblinear",penalty="l1",C=C);m.fit(xts,y);pr=m.predict_proba(xvs)[:,1]
    return metrics(test.realized_direction,np.where(pr>=.5,"bullish","bearish"),pr)

def permutation_best(args):
    perm_y,mats_by_family=args
    mx=-np.inf
    for fam,mats in mats_by_family.items():
        if not mats: continue
        for C in PERM_C:
            mx=max(mx,cv_score(mats,C,perm_y))
    return mx

def main():
    d=pd.read_csv(E);d.expiry_date=pd.to_datetime(d.expiry_date);d=d.sort_values("expiry_date").reset_index(drop=True)
    dev=d[d.expiry_date<pd.Timestamp("2026-01-01")].reset_index(drop=True)
    hold=d[d.expiry_date>=pd.Timestamp("2026-01-01")].reset_index(drop=True)
    g=groups(dev);y=(dev.realized_direction=="bullish").astype(int)

    # Precompute fold-specific imputation/scaling once. This is mathematically identical
    # to the previous Pipeline implementation but avoids repeating invariant preprocessing
    # across the 500 label permutations.
    mats_by_family={fam:make_mats(dev,cols) for fam,cols in g.items() if cols}
    cand=[]
    for fam,cols in g.items():
        if not cols:continue
        mats=mats_by_family[fam]
        for C in SCREEN_C:
            cand.append({"family":fam,"C":C,"cv_balanced_accuracy":cv_score(mats,C,y),"n_features":len(cols)})
    cand.sort(key=lambda z:(-z["cv_balanced_accuracy"],z["n_features"],z["family"]))
    best=cand[0]
    holdm=fit(dev,hold,g[best["family"]],best["C"])

    xt,xv,_=_prepare_train_test(dev,hold,g[best["family"]]);yy=(dev.realized_direction=="bullish").astype(int)
    scaler=StandardScaler();xts=scaler.fit_transform(xt);xvs=scaler.transform(xv)
    mm=LogisticRegression(max_iter=5000,solver="liblinear",penalty="l1",C=best["C"]);mm.fit(xts,yy)
    ppred=np.where(mm.predict_proba(xvs)[:,1]>=.5,"bullish","bearish")
    holdm["accuracy_bootstrap_95ci"]=bootstrap_accuracy(hold.realized_direction,ppred)
    holdm["tree_depth2"]=tree_holdout(dev,hold,g[best["family"]],2)

    rng=np.random.default_rng(12345)
    perms=[pd.Series(rng.permutation(y.to_numpy())) for _ in range(PERMUTATIONS)]
    jobs=[(yp,mats_by_family) for yp in perms]
    workers=max(1,min(2,os.cpu_count() or 1))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        perm=list(ex.map(permutation_best,jobs))
    obs=best["cv_balanced_accuracy"]
    pp=(1+sum(x>=obs for x in perm))/(1+len(perm))

    res={"protocol":{"all_available_strikes":True,"surface_grid":"ATM-relative -30..+30","development":"before 2026-01-01","holdout":"2026 onward","cv":"5-fold chronological","permutations":PERMUTATIONS,"permutation_candidates":"6 feature families x 3 C values","parallel_workers":workers},
         "coverage":{"development":len(dev),"holdout":len(hold),"median_strikes":float(d.available_strikes.median()),"min_strikes":int(d.available_strikes.min()),"max_strikes":int(d.available_strikes.max())},
         "selected_model":best,"holdout":holdm,"multiple_testing_permutation_p":float(pp),"top_screen":cand[:20]}
    J.write_text(json.dumps(res,indent=2)+"\n")
    lines=["# Phase 12 Full-Chain Analysis","",f"Development {len(dev)} events; 2026 holdout {len(hold)} events.",f"Available strikes/event: median {d.available_strikes.median():.0f}, range {d.available_strikes.min()}–{d.available_strikes.max()}.","", "## Selected model",json.dumps(best,indent=2),"","## 2026 holdout",json.dumps(holdm,indent=2), "",f"## Multiple-testing permutation p={pp:.4f}","","This is a full-chain screen. No trading translation is authorized without independent replication and robustness."]
    lines += ["","## Top screens","| Family | C | CV balanced accuracy | Features |","|---|---:|---:|---:|"]+[f"| {r['family']} | {r['C']} | {r['cv_balanced_accuracy']:.3f} | {r['n_features']} |" for r in cand[:10]]
    M.write_text("\n".join(lines)+"\n")

if __name__=="__main__":main()
