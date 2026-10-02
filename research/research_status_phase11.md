# Phase 11 Research Status

**Branch:** `phase-11-premium-direction-predictor`  
**Status:** Phase 5 — robustness/falsification; no premium-only trading signal has been validated.  
**Last updated:** 2026-10-02

## Phase status

| Phase | Status |
|---|---|
| 0 — Protocol freeze | COMPLETE |
| 1 — Data acquisition/validation | COMPLETE — 132 expiry candidates, 121 valid events |
| 2 — Feature engineering | COMPLETE |
| 3 — Primary directional test | COMPLETE — 61/121 = 50.41% |
| 4 — Chronological holdout | COMPLETE — 2026: 9/20 = 45.0% for original predictor |
| 5 — Robustness/falsification | IN PROGRESS — frozen call-wing ratios tested; independent-source replication code updated and awaiting fresh CI execution |
| 6 — Trading translation | NOT STARTED — gated by predictive validity |
| 7 — Manuscript/conclusion package | NOT STARTED — will be completed after Phase 5 gate |

## Dataset and provenance

- Primary event table: **121 valid weekly-expiry events** from October 2024 through the available 2026 sample.
- Acquisition candidates: 132 expiry events.
- Exclusions: 1 missing required option leg, 3 missing 10:00 NIFTY spot observations, 7 missing expiry-date spot observations.
- Primary observation convention: exact **10:00:00 IST one-minute bar OPEN** for NIFTY and the six option legs.
- Expiry outcome: latest NIFTY one-minute CLOSE on expiry as a provisional settlement proxy.
- NSE documentation states that final exercise settlement for index options uses the closing price of the relevant underlying index on the last trading day. citeturn2search0
- The current dataset therefore uses a transparent index-close proxy; an explicit historical NSE close cross-check remains a data-validation task.

## Primary predictor result

User-specified signal:
- Call score = CE OTM7 + CE OTM8 − CE OTM6.
- Put score = PE OTM7 + PE OTM8 − PE OTM6.
- Call score > Put score → bearish.
- Put score > Call score → bullish.

Results:
- 61/121 correct = **50.41%**.
- Exact binomial p = **1.000** against a 50% null.
- Bootstrap 95% accuracy CI = **41.32%–59.50%**.
- 2026 chronological holdout = **9/20 = 45.0%**.
- Overall Pearson spread/expiry-return correlation = **−0.2086, p=0.02165**, but Spearman rho = −0.1118 (p=0.22223), logistic slope p=0.22877, and 2026 holdout Pearson p=0.8154.
- Decision: the isolated Pearson relationship is exploratory/non-robust and is not promoted to trading.

## Formal premium-combination search

The search evaluated:
- 6 raw premiums.
- 78 engineered premium features.
- 156 threshold/mapping candidates.
- All 63 non-empty raw-premium logistic subsets.
- 5-fold development CV with 2026 held out chronologically.
- 5,000 permutations for the maximum-threshold-accuracy multiple-testing diagnostic.

Leading candidates:
- CE OTM6/OTM7 log-ratio: 59.41% development; 12/20 = 60.0% holdout.
- CE OTM6/OTM8 log-ratio: 59.41% development; 12/20 = 60.0% holdout.
- Best raw-premium subset logistic: CE OTM6 + CE OTM7 + PE OTM7; 50.38% development CV; 12/20 holdout.
- Multiple-testing diagnostic for maximum threshold accuracy: **p=0.5118**.
- Holdout class balance: 7 bullish / 13 bearish; always-bearish accuracy = 65%.

## Frozen-candidate robustness

Both call-wing ratios were frozen before additional tests.

| Test | CE OTM6/7 | CE OTM6/8 |
|---|---:|---:|
| Development | 60/101 = 59.41% | 60/101 = 59.41% |
| 2026 holdout | 12/20 = 60.0% | 12/20 = 60.0% |
| Expanding walk-forward | 64/101 = 63.37% | 63/101 = 62.38% |
| Pre-2025-09-01 | 53/85 = 62.35% | 53/85 = 62.35% |
| On/after 2025-09-01 | 19/36 = 52.78% | 19/36 = 52.78% |

Both candidates produce identical classifications on the 2026 holdout:
- 3 bullish predictions.
- 17 bearish predictions.
- Confusion matrix: TP=1, FP=2, FN=6, TN=11.
- Balanced accuracy = **49.45%**.
- Matthews correlation coefficient ≈ **−0.0147**.
- Thus the 60% raw accuracy is largely a consequence of the bearish class imbalance and does not demonstrate useful discrimination.

## Independent source audit

Previous cross-source audit:
- 82 eligible overlapping events.
- 81/82 had a secondary-source match = **98.78%**.
- All 81 matched events had all six required legs.
- Mean relative price difference = **0.3045%**.

A correction was made to the audit code:
1. The persisted median-relative-difference statistic was corrected to use the event-level median column.
2. Frozen-candidate replication now matches realized direction by both expiry and observation timestamp.

A fresh CI execution is required before the corrected replication metrics are used in the manuscript.

## Current scientific interpretation

The evidence does **not** establish a stable premium-only NIFTY direction predictor at 4-DTE/10:00.

The strongest lead is a relative call-wing ratio, but:
- it was discovered after a broad feature search;
- its maximum-threshold multiple-testing diagnostic is non-significant;
- its final holdout is only 20 events;
- it does not beat the 65% always-bearish accuracy baseline;
- balanced accuracy and MCC are approximately chance;
- performance deteriorates after the September 2025 expiry-convention boundary.

Therefore **no trading strategy is authorized from Phase 11**.

## Remaining Phase 5 gate

1. Execute the corrected independent-source replication.
2. Validate expiry outcomes against NSE historical index closes/settlement documentation.
3. Preserve the primary 10:00-open convention and test timestamp/quote sensitivity only where raw data exists.
4. If replication remains null/weak, close Phase 5 with a negative/inconclusive conclusion and produce the final manuscript package.
5. Do not mine additional premium formulas unless a separately pre-registered research question is created; this prevents repeated data-snooping.

## Research completion rule

If the remaining validation does not materially change the evidence, Phase 6 trading translation will remain **not started**, because the protocol requires credible out-of-sample predictive validity before economic testing. The final package will then report the negative/unstable result, data limitations, strengths, and future research directions rather than forcing a trading strategy.
