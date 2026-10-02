import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest


EVENTS = Path("results/phase11_events.csv")
OUT_JSON = Path("results/phase11_robustness.json")
OUT_MD = Path("results/phase11_robustness.md")


def accuracy(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.mean(y_true == y_pred)) if len(y_true) else None


def p50(correct, n):
    return float(binomtest(correct, n, 0.5).pvalue) if n else None


def eval_binary(df, pred_col="pred", y_col="y"):
    x = df[[pred_col, y_col]].dropna()
    n = len(x)
    correct = int((x[pred_col] == x[y_col]).sum())
    return {
        "n": n,
        "correct": correct,
        "accuracy": accuracy(x[y_col], x[pred_col]),
        "exact_binomial_p_50": p50(correct, n),
    }


def classification_metrics(y_true, y_pred):
    y = pd.Series(y_true).astype(str)
    p = pd.Series(y_pred).astype(str)
    tp = int(((p == "bullish") & (y == "bullish")).sum())
    fp = int(((p == "bullish") & (y == "bearish")).sum())
    fn = int(((p == "bearish") & (y == "bullish")).sum())
    tn = int(((p == "bearish") & (y == "bearish")).sum())
    tpr = tp / (tp + fn) if tp + fn else None
    tnr = tn / (tn + fp) if tn + fp else None
    bal = (tpr + tnr) / 2 if tpr is not None and tnr is not None else None
    denom = ((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)) ** 0.5
    mcc = ((tp * tn - fp * fn) / denom) if denom else None
    return {"tp_bullish": tp, "fp_bullish": fp, "fn_bullish": fn, "tn_bearish": tn,
            "balanced_accuracy": bal, "matthews_corrcoef": mcc}


def threshold_from_train(train, feature):
    return float(train[feature].median())


def make_predictions(df, feature, threshold, mapping):
    # Frozen convention for the selected candidates: high ratio => bullish.
    if mapping == "high_bull":
        return np.where(df[feature] >= threshold, "bullish", "bearish")
    return np.where(df[feature] >= threshold, "bearish", "bullish")


def expanding_eval(df, feature, mapping="high_bull", min_train=20):
    rows = []
    work = df.sort_values("expiry_date").reset_index(drop=True)
    for i in range(min_train, len(work)):
        train = work.iloc[:i]
        test = work.iloc[i:i+1]
        threshold = threshold_from_train(train, feature)
        pred = make_predictions(test, feature, threshold, mapping)[0]
        rows.append({
            "expiry_date": str(test.iloc[0]["expiry_date"]),
            "threshold": threshold,
            "prediction": pred,
            "realized": test.iloc[0]["realized_direction"],
            "correct": bool(pred == test.iloc[0]["realized_direction"]),
        })
    r = pd.DataFrame(rows)
    if r.empty:
        return {"n": 0, "correct": 0, "accuracy": None, "exact_binomial_p_50": None}
    return {
        "n": int(len(r)),
        "correct": int(r["correct"].sum()),
        "accuracy": float(r["correct"].mean()),
        "exact_binomial_p_50": p50(int(r["correct"].sum()), len(r)),
        "first_test_date": str(r["expiry_date"].iloc[0]),
        "last_test_date": str(r["expiry_date"].iloc[-1]),
    }


def fixed_threshold_eval(df, feature, threshold, mapping="high_bull"):
    work = df.copy()
    work["y"] = work["realized_direction"]
    work["pred"] = make_predictions(work, feature, threshold, mapping)
    return eval_binary(work)


def regime_eval(df, feature, threshold, mapping="high_bull"):
    out = {}
    work = df.copy()
    work["y"] = work["realized_direction"]
    work["pred"] = make_predictions(work, feature, threshold, mapping)
    work["year"] = pd.to_datetime(work["expiry_date"]).dt.year
    work["expiry_regime"] = np.where(
        pd.to_datetime(work["expiry_date"]) < pd.Timestamp("2025-09-01"),
        "pre_2025_09_01",
        "post_2025_09_01",
    )
    for key, g in work.groupby("year"):
        out[f"year_{key}"] = eval_binary(g)
    for key, g in work.groupby("expiry_regime"):
        out[key] = eval_binary(g)
    return out


def main():
    df = pd.read_csv(EVENTS)
    df["expiry_date"] = pd.to_datetime(df["expiry_date"])
    dev = df[df["expiry_date"] < pd.Timestamp("2026-01-01")].copy()
    hold = df[df["expiry_date"] >= pd.Timestamp("2026-01-01")].copy()

    candidates = {
        "ce_otm6_ce_otm7_logratio": "logratio__ce_otm6__ce_otm7",
        "ce_otm6_ce_otm8_logratio": "logratio__ce_otm6__ce_otm8",
    }

    result = {
        "protocol": {
            "development": "expiry before 2026-01-01",
            "holdout": "expiry on/after 2026-01-01",
            "candidate_mapping": "high ratio => bullish",
            "threshold_rule": "development median; no holdout tuning",
            "expanding_rule": "median of all prior observations; minimum training window 20 events",
            "regime_splits": ["calendar year", "pre/post 2025-09-01 expiry-convention boundary"],
        },
        "candidates": {},
    }

    for name, feature in candidates.items():
        threshold = threshold_from_train(dev, feature)
        result["candidates"][name] = {
            "feature": feature,
            "development_threshold": threshold,
            "development": fixed_threshold_eval(dev, feature, threshold),
            "holdout_2026": {**fixed_threshold_eval(hold, feature, threshold), "classification_metrics": classification_metrics(hold["realized_direction"], make_predictions(hold, feature, threshold, "high_bull"))},
            "full_sample_regimes": regime_eval(df, feature, threshold),
            "expanding_validation_full_sample": expanding_eval(df, feature, "high_bull", 20),
        }

    # Compare the two frozen candidates by agreement and by a simple average vote.
    a = candidates["ce_otm6_ce_otm7_logratio"]
    b = candidates["ce_otm6_ce_otm8_logratio"]
    ta = threshold_from_train(dev, a)
    tb = threshold_from_train(dev, b)
    h = hold.copy()
    pa = make_predictions(h, a, ta, "high_bull")
    pb = make_predictions(h, b, tb, "high_bull")
    vote = np.where(pa == pb, pa, "bearish")  # abstention-to-baseline diagnostic only
    result["holdout_candidate_agreement"] = {
        "n": int(len(h)),
        "same_prediction_count": int(np.sum(pa == pb)),
        "same_prediction_fraction": float(np.mean(pa == pb)),
        "both_high_ratio_bullish_count": int(np.sum((pa == "bullish") & (pb == "bullish"))),
        "both_low_ratio_bearish_count": int(np.sum((pa == "bearish") & (pb == "bearish"))),
        "conservative_bearish_vote_accuracy": accuracy(h["realized_direction"], vote),
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")

    lines = [
        "# Phase 11 Robustness / Falsification",
        "",
        "Two candidates were frozen before robustness testing: CE OTM6/OTM7 and CE OTM6/OTM8 log-ratios. The mapping is high ratio = bullish. Thresholds are the 2024–2025 development medians and are never tuned on the 2026 holdout.",
        "",
        "## Frozen-candidate results",
        "",
        "| Candidate | Dev accuracy | Dev p(50%) | 2026 holdout | Holdout p(50%) | Expanding accuracy |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, r in result["candidates"].items():
        d = r["development"]
        h = r["holdout_2026"]
        e = r["expanding_validation_full_sample"]
        lines.append(
            f"| {name} | {d['accuracy']:.2%} | {d['exact_binomial_p_50']:.4f} | "
            f"{h['accuracy']:.2%} ({h['correct']}/{h['n']}) | {h['exact_binomial_p_50']:.4f} | "
            f"{e['accuracy']:.2%} ({e['correct']}/{e['n']}) |"
        )

    lines += [
        "",
        "## Regime splits",
        "",
    ]
    for name, r in result["candidates"].items():
        lines.append(f"### {name}")
        for regime, v in r["full_sample_regimes"].items():
            lines.append(f"- {regime}: {v['accuracy']:.2%} ({v['correct']}/{v['n']}), p={v['exact_binomial_p_50']:.4f}")
        lines.append("")

    ag = result["holdout_candidate_agreement"]
    lines += [
        "## Candidate agreement",
        f"- The two frozen ratios make the same prediction on {ag['same_prediction_count']}/{ag['n']} holdout events ({ag['same_prediction_fraction']:.2%}).",
        f"- Both are bullish on {ag['both_high_ratio_bullish_count']} holdout events and both bearish on {ag['both_low_ratio_bearish_count']} events.",
        "",
        "## Holdout class-imbalance diagnostics",
        "",
        "The 2026 holdout contains 7 bullish and 13 bearish realized outcomes. For both frozen ratios the confusion matrix is TP=1, FP=2, FN=6, TN=11, giving balanced accuracy 49.45% and Matthews correlation -0.0147. These metrics are below what raw accuracy alone suggests.",
        "",
        "## Interpretation",
        "The frozen call-wing ratios remain a research lead, but this robustness package does not establish a stable predictor. The 2026 holdout has only 20 observations; the two ratios are highly overlapping constructions; and the earlier multiple-testing diagnostic was non-significant. The expanding validation is especially important because it avoids using future observations to set thresholds.",
        "",
        "Data limitations: the current event table does not contain contemporaneous bid/ask, option volume/OI, India VIX, or alternate 10:00 timestamp bars. Those planned robustness dimensions therefore require additional raw datasets before they can be tested honestly.",
        "",
        "Decision: continue Phase 5 only for pre-specified falsification/replication. No trading translation is authorized from these results.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
