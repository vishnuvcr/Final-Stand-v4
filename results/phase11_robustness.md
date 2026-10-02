# Phase 11 Robustness / Falsification

Two candidates were frozen before robustness testing: CE OTM6/OTM7 and CE OTM6/OTM8 log-ratios. The mapping is high ratio = bullish. Thresholds are the 2024–2025 development medians and were not tuned on the 2026 holdout.

## Frozen-candidate results

| Candidate | Development | 2026 holdout | Expanding walk-forward |
|---|---:|---:|---:|
| CE OTM6/OTM7 log-ratio | 60/101 = 59.41% (p=0.0728) | 12/20 = 60.0% (p=0.5034) | 64/101 = 63.37% (p=0.0093) |
| CE OTM6/OTM8 log-ratio | 60/101 = 59.41% (p=0.0728) | 12/20 = 60.0% (p=0.5034) | 63/101 = 62.38% (p=0.0165) |

The expanding-walk-forward p-values are unadjusted exploratory values and do not override the final chronological holdout or the earlier multiple-testing diagnostic.

## Regime split

The two ratios generate identical classifications for the current event table, so their regime results are identical.

- 2024: 32/50 = 64.0%, p=0.0649.
- 2025: 28/51 = 54.90%, p=0.5758.
- 2026: 12/20 = 60.0%, p=0.5034.
- Expiry before 2025-09-01: 53/85 = 62.35%, p=0.0295.
- Expiry on/after 2025-09-01: 19/36 = 52.78%, p=0.8679.

The deterioration after the September 2025 NIFTY expiry-convention boundary is a key robustness concern. It prevents treating the earlier 62%+ accuracy as a stable cross-regime effect.

## 2026 holdout classification structure

Both ratios give exactly the same prediction on all 20 holdout events:

- 3 bullish predictions.
- 17 bearish predictions.
- Confusion matrix: 1 bullish predicted / bullish realized; 2 bullish predicted / bearish realized; 6 bearish predicted / bullish realized; 11 bearish predicted / bearish realized.

Thus the 60% accuracy comes largely from predicting bearish on an imbalanced holdout, where the always-bearish baseline is 65%. The ratio signal does not improve that baseline in the current holdout.

## Interpretation

There is a potentially interesting historical pattern in the relative call-wing premium ratios. The expanding analysis is directionally encouraging, but the effect is not stable across the expiry-convention regime: pre-September-2025 accuracy is 62.35%, while the post-boundary sample is 52.78%. The final 2026 holdout is only 20 events and is not statistically distinguishable from 50% by the exact binomial test.

Combined with the earlier 5,000-permutation multiple-testing diagnostic (p=0.5118), the evidence is insufficient to promote this signal to a trading strategy.

## Missing robustness dimensions

The current event table does not contain contemporaneous bid/ask, option volume/OI, India VIX, or alternate 10:00 timestamp bars. Those planned robustness dimensions require additional raw datasets before they can be tested without inventing or proxying data.

**Decision:** remain in Phase 5. No trading translation is authorized.
