# Phase 12 Full-Chain Analysis

Development 101 events; 2026 holdout 20 events.
Available strikes/event: median 89, range 58–127.

## Selected model
{
  "family": "volume_only",
  "C": 1.0,
  "cv_balanced_accuracy": 0.5671212121212121,
  "n_features": 136
}

## 2026 holdout
{
  "n": 20,
  "correct": 7,
  "accuracy": 0.35,
  "balanced_accuracy": 0.4010989010989011,
  "mcc": -0.2058790548922549,
  "exact_binomial_p_50": 0.26317596435546875,
  "roc_auc": 0.43956043956043955,
  "accuracy_bootstrap_95ci": [
    0.15,
    0.55
  ],
  "tree_depth2": {
    "n": 20,
    "correct": 7,
    "accuracy": 0.35,
    "balanced_accuracy": 0.46703296703296704,
    "mcc": -0.10482848367219183,
    "exact_binomial_p_50": 0.26317596435546875,
    "roc_auc": 0.4395604395604395
  }
}

## Multiple-testing permutation p=0.4331

This is a full-chain screen. No trading translation is authorized without independent replication and robustness.

## Top screens
| Family | C | CV balanced accuracy | Features |
|---|---:|---:|---:|
| volume_only | 1.0 | 0.567 | 136 |
| volume_only | 0.3 | 0.545 | 136 |
| oi_only | 0.1 | 0.524 | 136 |
| oi_only | 1.0 | 0.518 | 136 |
| oi_only | 0.3 | 0.512 | 136 |
| aggregate | 0.01 | 0.500 | 26 |
| aggregate | 0.03 | 0.500 | 26 |
| aggregate | 0.1 | 0.500 | 26 |
| oi_only | 0.01 | 0.500 | 136 |
| oi_only | 0.03 | 0.500 | 136 |
