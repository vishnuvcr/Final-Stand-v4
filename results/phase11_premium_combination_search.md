# Phase 11 Premium Combination Search

## Protocol
- Development sample: expiry before 2026-01-01.
- Holdout: expiry on/after 2026-01-01.
- Six raw premiums: CE/PE OTM6, OTM7, OTM8.
- Engineered candidate features: 78.
- Raw-premium subset logistic models: 63 (all non-empty subsets).
- Threshold models: 156.
- Threshold selection and diagnostics use development data; the 2026 sample is chronological holdout.
- Permutation repetitions for the multiple-testing diagnostic: 5000.
- Selection rule for subset models: highest 5-fold development CV accuracy, with fewer raw premiums preferred on ties.

## Selected threshold candidate
**Feature:** `logratio__ce_otm6__ce_otm7`  
**Mapping:** high_bull

- Development accuracy: 59.41%
- Development exact binomial p-value: 0.0728
- 2026 holdout accuracy: 60.00% (12/20)

The leading threshold structures are mainly **relative call-wing measures**. Two top candidates, CE OTM6/OTM7 and CE OTM6/OTM8 log-ratios, each achieved 59.41% development accuracy and 12/20 (60%) on the 2026 holdout.

## Selected raw-premium subset logistic model
**Features:** `ce_otm6+ce_otm7+pe_otm7`

- Features: 3
- Development 5-fold CV accuracy: 50.38%
- Development fitted accuracy: 57.43%
- Development exact binomial p-value: 0.1633
- 2026 holdout accuracy: 60.00% (12/20)

The subset search therefore did **not** identify a strong development-time cross-validated model. The 60% holdout result is not sufficient to establish predictive power.

## Multiple-testing diagnostic
- Permutation p-value for the maximum threshold accuracy across the searched threshold library: **0.5118**.
- This is far from conventional evidence against a null of no directional information after accounting for the search.

## Holdout baseline
- Always-bullish: 35.00%
- Always-bearish: 65.00%
- Holdout n: 20

The selected threshold candidate's 60% holdout accuracy is below the 65% always-bearish class-frequency baseline. Accuracy alone therefore does not establish economic usefulness.

## Top threshold candidates
| Feature | Mapping | Development accuracy | Development p | 2026 holdout |
|---|---|---:|---:|---:|
| `logratio__ce_otm6__ce_otm8` | high_bull | 59.41% | 0.0728 | 60.00% (12/20) |
| `logratio__ce_otm6__ce_otm7` | high_bull | 59.41% | 0.0728 | 60.00% (12/20) |
| `logratio__ce_otm7__ce_otm8` | high_bull | 57.43% | 0.1633 | 60.00% (12/20) |
| `diff__ce_otm7__pe_otm8` | high_bear | 56.44% | 0.2323 | 50.00% (10/20) |
| `cpdiff__ce_otm7__pe_otm8` | high_bear | 56.44% | 0.2323 | 50.00% (10/20) |
| `logratio__ce_otm7__pe_otm8` | high_bear | 56.44% | 0.2323 | 60.00% (12/20) |
| `cpratio__ce_otm7__pe_otm8` | high_bear | 56.44% | 0.2323 | 60.00% (12/20) |

## Interpretation
The search finds a **repeatable-looking but weak lead** in relative call-wing premiums: ratios involving CE OTM6 versus CE OTM7/OTM8 reached 60% on the 20-event holdout. However:
1. the holdout contains only 20 events;
2. many feature/mapping combinations were searched;
3. the permutation multiple-testing diagnostic is not significant;
4. the subset logistic search has development CV accuracy near 50%;
5. the 60% holdout accuracy is below the 65% always-bearish class-frequency baseline.

**Decision:** do not promote any premium-only combination to a trading strategy yet. Continue Phase 5 robustness/falsification with pre-specified call-wing ratios, rolling/expanding validation, regime splits, liquidity filters, and independent-source replication before any trading translation.
