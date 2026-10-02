#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

PREMIUMS = ["ce_otm6", "ce_otm7", "ce_otm8", "pe_otm6", "pe_otm7", "pe_otm8"]
EPS = 1e-8
SEED = 20261002


def logistic_fit(X: np.ndarray, y: np.ndarray, l2: float = 0.25) -> np.ndarray:
    X1 = np.column_stack([np.ones(len(X)), X])
    beta = np.zeros(X1.shape[1])
    penalty = np.eye(X1.shape[1]) * l2
    penalty[0, 0] = 0.0
    for _ in range(100):
        z = np.clip(X1 @ beta, -30, 30)
        p = 1 / (1 + np.exp(-z))
        w = p * (1 - p)
        H = X1.T @ (w[:, None] * X1) + penalty
        g = X1.T @ (y - p) - penalty @ beta
        step = np.linalg.solve(H, g)
        beta += step
        if np.max(np.abs(step)) < 1e-9:
            break
    return beta


def predict(X: np.ndarray, beta: np.ndarray) -> np.ndarray:
    X1 = np.column_stack([np.ones(len(X)), X])
    return 1 / (1 + np.exp(-np.clip(X1 @ beta, -30, 30)))


def acc(y, p):
    return float((y == (p >= 0.5)).mean())


def binom_p(k, n):
    return float(stats.binomtest(int(k), int(n), 0.5).pvalue)


def add_simple_features(df: pd.DataFrame) -> pd.DataFrame:
    out = {}
    x = {c: pd.to_numeric(df[c], errors="coerce") for c in PREMIUMS}

    for c in PREMIUMS:
        out[c] = x[c]

    calls = ["ce_otm6", "ce_otm7", "ce_otm8"]
    puts = ["pe_otm6", "pe_otm7", "pe_otm8"]

    for a, b in itertools.combinations(PREMIUMS, 2):
        out[f"diff__{a}__{b}"] = x[a] - x[b]
        out[f"sum__{a}__{b}"] = x[a] + x[b]
        out[f"logratio__{a}__{b}"] = np.log((x[a] + EPS) / (x[b] + EPS))

    for c in calls:
        for p in puts:
            out[f"cpdiff__{c}__{p}"] = x[c] - x[p]
            out[f"cpratio__{c}__{p}"] = np.log((x[c] + EPS) / (x[p] + EPS))

    out["call_mean"] = df[calls].mean(axis=1)
    out["put_mean"] = df[puts].mean(axis=1)
    out["call_put_mean_diff"] = out["call_mean"] - out["put_mean"]
    out["call_put_mean_logratio"] = np.log((out["call_mean"] + EPS) / (out["put_mean"] + EPS))
    out["call_slope_6_8"] = x["ce_otm8"] - x["ce_otm6"]
    out["put_slope_6_8"] = x["pe_otm8"] - x["pe_otm6"]
    out["wing_gap"] = (x["ce_otm6"] + x["pe_otm6"]) - (x["ce_otm8"] + x["pe_otm8"])
    out["inner_gap"] = (x["ce_otm6"] + x["pe_otm6"]) - (x["ce_otm7"] + x["pe_otm7"])
    out["outer_gap"] = (x["ce_otm7"] + x["pe_otm7"]) - (x["ce_otm8"] + x["pe_otm8"])

    return pd.DataFrame(out, index=df.index).replace([np.inf, -np.inf], np.nan)


def threshold_search(train_x, train_y, test_x, test_y):
    results = []
    for name in train_x.columns:
        x = train_x[name].to_numpy(float)
        xt = test_x[name].to_numpy(float)
        med = float(np.median(x))
        for direction in ("high_bull", "high_bear"):
            pred_train = x >= med
            if direction == "high_bear":
                pred_train = ~pred_train
            results.append({
                "family": "threshold",
                "feature": name,
                "mapping": direction,
                "train_accuracy": float((train_y == pred_train).mean()),
                "train_p": binom_p((train_y == pred_train).sum(), len(train_y)),
                "test_accuracy": float((test_y == ((xt >= med) if direction == "high_bull" else ~(xt >= med))).mean()),
                "test_correct": int((test_y == ((xt >= med) if direction == "high_bull" else ~(xt >= med))).sum()),
            })
    return pd.DataFrame(results)


def subset_logistic_search(train_df, test_df, y_train, y_test):
    rows = []
    Xraw = train_df[PREMIUMS].to_numpy(float)
    Traw = test_df[PREMIUMS].to_numpy(float)
    for r in range(1, len(PREMIUMS) + 1):
        for cols in itertools.combinations(range(len(PREMIUMS)), r):
            names = [PREMIUMS[i] for i in cols]
            mu = Xraw[:, cols].mean(axis=0)
            sd = Xraw[:, cols].std(axis=0, ddof=0)
            sd[sd < 1e-12] = 1.0
            X = (Xraw[:, cols] - mu) / sd
            T = (Traw[:, cols] - mu) / sd

            folds = np.array_split(np.arange(len(y_train)), 5)
            cv_scores = []
            for val_idx in folds:
                tr_idx = np.setdiff1d(np.arange(len(y_train)), val_idx)
                beta = logistic_fit(X[tr_idx], y_train[tr_idx])
                cv_scores.append(acc(y_train[val_idx], predict(X[val_idx], beta)))
            cv_acc = float(np.mean(cv_scores))

            beta = logistic_fit(X, y_train)
            train_prob = predict(X, beta)
            test_prob = predict(T, beta)
            rows.append({
                "family": "subset_logistic",
                "feature": "+".join(names),
                "n_features": r,
                "cv_accuracy": cv_acc,
                "train_accuracy": acc(y_train, train_prob),
                "train_p": binom_p(int((y_train == (train_prob >= .5)).sum()), len(y_train)),
                "test_accuracy": acc(y_test, test_prob),
                "test_correct": int((y_test == (test_prob >= .5)).sum()),
                "test_n": len(y_test),
            })
    return pd.DataFrame(rows)


def main():
    df = pd.read_csv("results/phase11_events.csv")
    df["expiry_date"] = pd.to_datetime(df["expiry_date"])
    df["y"] = (df["realized_direction"] == "bullish").astype(int)
    train = df[df.expiry_date < "2026-01-01"].copy()
    test = df[df.expiry_date >= "2026-01-01"].copy()

    feats = add_simple_features(train)
    test_feats = add_simple_features(test)
    valid = feats.columns[feats.notna().all() & test_feats.notna().all()]
    feats = feats[valid]
    test_feats = test_feats[valid]

    ytr = train.y.to_numpy()
    yte = test.y.to_numpy()
    thresholds = threshold_search(feats, ytr, test_feats, yte)
    subset = subset_logistic_search(train, test, ytr, yte)

    subset_sorted = subset.sort_values(["cv_accuracy", "n_features", "feature"], ascending=[False, True, True]).reset_index(drop=True)
    selected = subset_sorted.iloc[0].to_dict()
    threshold_sorted = thresholds.sort_values(["train_accuracy", "feature", "mapping"], ascending=[False, True, True]).reset_index(drop=True)
    selected_threshold = threshold_sorted.iloc[0].to_dict()

    rng = np.random.default_rng(SEED)
    observed = float(threshold_sorted.iloc[0]["train_accuracy"])
    null_max = []
    feature_matrix = feats.to_numpy(float)
    medians = np.nanmedian(feature_matrix, axis=0)
    for _ in range(5000):
        yp = rng.permutation(ytr)
        best = 0.0
        for j in range(feature_matrix.shape[1]):
            pred = feature_matrix[:, j] >= medians[j]
            best = max(best, float((yp == pred).mean()), float((yp == ~pred).mean()))
        null_max.append(best)
    max_perm_p = float((np.asarray(null_max) >= observed).mean())

    out = {
        "protocol": {
            "development": "expiry before 2026-01-01",
            "holdout": "expiry on/after 2026-01-01",
            "candidate_features": len(valid),
            "raw_premium_count": 6,
            "subset_models": len(subset),
            "threshold_models": len(thresholds),
            "selection_rule": "highest 5-fold development CV accuracy; ties prefer fewer raw premiums",
            "permutation_repetitions": 5000,
        },
        "selected_threshold": selected_threshold,
        "selected_subset_logistic": selected,
        "best_threshold_rows": thresholds.sort_values("train_accuracy", ascending=False).head(20).to_dict("records"),
        "best_subset_rows": subset_sorted.head(20).to_dict("records"),
        "multiple_testing_threshold_max_accuracy_p": max_perm_p,
        "holdout_baselines": {
            "always_bullish": float(yte.mean()),
            "always_bearish": float(1 - yte.mean()),
            "n": len(yte),
        },
    }

    Path("results/phase11_premium_combination_search.json").write_text(json.dumps(out, indent=2) + "\n")
    lines = [
        "# Phase 11 Premium Combination Search",
        "",
        f"- Development events: {len(train)}",
        f"- 2026 chronological holdout: {len(test)}",
        f"- Candidate engineered features: {len(valid)}",
        f"- Threshold models: {len(thresholds)}",
        f"- All non-empty raw-premium subsets: {len(subset)}",
        "",
        "## Selection rule",
        "Models are selected using development-period 5-fold cross-validation only. The 2026 holdout is not used for feature/formula selection.",
        "",
        "## Best threshold candidate",
        f"- Feature: {selected_threshold['feature']}",
        f"- Mapping: {selected_threshold['mapping']}",
        f"- Development accuracy: {selected_threshold['train_accuracy']:.4f}",
        f"- 2026 holdout accuracy: {selected_threshold['test_accuracy']:.4f}",
        "",
        "## Best raw-premium subset logistic model",
        f"- Features: {selected['feature']}",
        f"- Development CV accuracy: {selected['cv_accuracy']:.4f}",
        f"- Development fitted accuracy: {selected['train_accuracy']:.4f}",
        f"- 2026 holdout accuracy: {selected['test_accuracy']:.4f}",
        "",
        "## Multiple-testing diagnostic",
        f"- Permutation p-value for maximum threshold accuracy across the entire engineered feature library: {max_perm_p:.6f}",
        "",
        "The holdout result is the relevant out-of-sample result. No candidate is promoted to a trading strategy merely because it ranked highly during development.",
    ]
    Path("results/phase11_premium_combination_search.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
