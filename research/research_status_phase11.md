# Phase 11 Research Status

**Branch:** phase-11-premium-direction-predictor  
**Status:** Phase 5 — robustness/falsification in progress; primary and holdout directional tests completed; no trading translation yet.  
**Last updated:** 2026-10-02

## Phase status

| Phase | Status |
|---|---|
| 0 — Protocol freeze | COMPLETE |
| 1 — Data acquisition/validation | COMPLETE — PRIMARY + INDEPENDENT CROSS-SOURCE AUDIT |
| 2 — Feature engineering | COMPLETE — 121 VALID EVENTS BUILT |
| 3 — Primary directional test | COMPLETE — 61/121 CORRECT (50.41%) |
| 4 — Out-of-sample validation | COMPLETE — 2026 HOLDOUT 9/20 (45.0%) |
| 5 — Robustness/falsification | IN PROGRESS |
| 6 — Trading translation | NOT STARTED |
| 7 — Manuscript/conclusion | NOT STARTED |

## Completed in this branch

- Created a separate Phase 11 branch.
- Recorded the exact user-specified premium formulas and directional mapping.
- Completed an initial literature/source review.
- Identified candidate intraday option and NIFTY spot sources.
- Added cached data-acquisition code for NIFTY option Parquet files and NIFTY 1-minute spot CSV files.
- Added the core predictor implementation with unit tests.
- Added an event builder that constructs the 4-DTE/10:00 event table from cached data.
- Added a manual GitHub Actions workflow with validate/acquire/build actions.
- Adopted a point-in-time 10:00 bar-open convention for the primary predictor.

## Latest execution checkpoint — 2026-10-02

- The primary public intraday candidate was independently verified: NIFTY 1-minute option data begins in October 2024 and is partitioned by year. citeturn2search0turn2search3
- Direct acquisition from this chat runtime failed because external DNS/network access to Hugging Face is unavailable.
- The GitHub connector can inspect Actions runs but does not expose the workflow-dispatch write endpoint; the new Phase 11 workflow therefore could not be programmatically started from this chat.
- Existing project/library NIFTY option artifacts were inspected. They are primarily EOD/contract-wise and therefore are not substituted for the required point-in-time 10:00 intraday observations.
- No performance result has been generated or inferred.

## Latest validation note

- Core signal tests and event-builder helper tests are committed. Direct local execution is unavailable in the current container because raw GitHub DNS resolution failed; GitHub Actions remains the execution environment for these tests.

## Data coverage state

No historical event dataset has yet been executed or validated in this branch. Therefore there is **no performance result yet**.

## Current blockers

1. Run the manual acquisition workflow with the required historical years.
2. Validate downloaded option/spot coverage and source schema.
3. Build the event dataset and independently verify a sample of events.
4. Only then run the statistical predictor tests.

## Research-completion rule

The study stops after the defined Phase 7 package. Conclusions will distinguish statistical evidence, economic magnitude, and data-quality uncertainty.


## 2026-10-02 — Expanded source search

A broad public-web search identified multiple independent 1-minute NIFTY option sources. Strong candidates now include OptionsData.shop, Unfluke, ICICI Direct Breeze pipelines, Shoonya/Cloud Trader Pro, MoneyTicks, and community archives; institutional candidates include NSE snapshot feeds, TrueData and Global Datafeeds. Broker APIs including Zerodha, Upstox, Angel One and DhanHQ were also catalogued with their expired-contract limitations. Full inventory: research/phase11/source_inventory.md.

Next gate: acquire and sample-audit at least two independent sources before selecting the Phase 11 primary dataset. Required checks are exact 10:00 IST coverage, expired contracts, CE/PE strikes, timestamp semantics, duplicates/missing bars, and cross-source price agreement.


## 2026-10-02 — Multi-source acquisition upgrade

A second independent public 1-minute archive was identified and incorporated: Hugging Face `thetrademarkk/india-index-options-1m`. Its dataset documentation reports 377M rows, NIFTY/BANKNIFTY/SENSEX 1-minute option bars, IST timestamps, OHLCV+OI, expiry-partitioned Parquet files, and a NIFTY 1-minute spot Parquet file. Option coverage is explicitly described as partial for illiquid/far strikes, so the Phase 11 event coverage audit remains mandatory.

The acquisition pipeline now:
1. downloads TradeMarkk NIFTY expiry-partitioned files for requested years as the primary source;
2. downloads TradeMarkk NIFTY 1-minute spot as the primary spot source;
3. retains the Rissin/Upstox archive as an independent secondary option cross-check;
4. retains the previous public spot source as an independent spot cross-check;
5. builds events from the primary source only unless a cross-source audit explicitly promotes/changes the source.

The GitHub Actions workflow now automatically performs acquisition and event building on pushes to this Phase 11 branch, while preserving manual `validate`, `acquire`, and `build` controls.

No predictive accuracy, p-value, correlation, or trading result has been calculated yet.


## 2026-10-02 — Phase 3/4 empirical results

### Dataset coverage
- 132 expiry candidates were evaluated.
- 121 valid 4-DTE/10:00 events were built.
- Exclusions: 1 missing required option leg, 3 missing 10:00 spot observations, 7 missing expiry-date spot observations.
- Predictions: 101 bullish, 20 bearish.
- Realized directions: 55 bullish, 66 bearish.

### Primary directional test
- Correct: 61/121.
- Accuracy: 50.41%.
- Exact two-sided binomial p-value against 50%: 1.000.
- Bootstrap 95% CI: 41.32%–59.50%.
- Always-bearish baseline: 54.55%; always-bullish baseline: 45.45%.
- Therefore the pre-specified directional mapping does not show evidence of a reliable directional edge in this sample.

### Continuous-score analysis
- Pearson correlation between premium spread and expiry return: r = -0.2086, p = 0.02165.
- Spearman correlation: rho = -0.1118, p = 0.22223.
- Logistic slope for realized bullish direction: -0.01801, p = 0.22877; 95% CI [-0.04734, 0.01132].
- The statistically smaller Pearson result is not supported by the rank correlation, logistic model, or chronological holdout, so it is not treated as robust evidence.

### Chronological holdout
- Development 2024–2025: 52/101 = 51.49%.
- 2026 holdout: 9/20 = 45.0%.
- 2026 holdout exact binomial p-value: 0.8238.
- Holdout spread/return Pearson r = -0.0558, p = 0.8154.
- Holdout logistic slope p = 0.6055.

### Independent source audit
The secondary Rissin/Upstox archive was checked for eligible events from October 2024 onward:
- 82 eligible events.
- 81/82 had at least one secondary price match (98.78%).
- All 81 matched events had all six required CE/PE legs.
- Mean absolute price difference: 0.1712 premium points.
- Mean relative price difference: 0.3045%.

This supports cross-source consistency of the point-in-time premium observations for the overlapping period, while not proving exchange-level correctness.

### Current inference
The Phase 11 primary hypothesis has **not** demonstrated stable out-of-sample directional predictive power. The isolated overall Pearson relationship is treated as exploratory because it does not survive the chronological holdout and is not corroborated by the rank/logistic tests.

Phase 5 robustness/falsification remains required before any trading translation.


## 2026-10-02 — Premium combination search results

The formal search completed successfully on GitHub Actions. It evaluated 78 engineered candidate features, 156 threshold/mapping models, and all 63 non-empty subsets of the six raw premiums, with a 2024–2025 development sample and 2026 chronological holdout.

- Best threshold candidates: CE OTM6/OTM7 and CE OTM6/OTM8 log-ratios, development accuracy 59.41%, 2026 holdout 60% (12/20).
- Selected subset logistic model: CE OTM6 + CE OTM7 + PE OTM7; 5-fold development CV accuracy 50.38%, 2026 holdout 60% (12/20).
- Multiple-testing permutation diagnostic for the maximum threshold accuracy: p = 0.5118.
- Holdout class-frequency baselines: always bullish 35%, always bearish 65%.

Inference: relative call-wing premium ratios are a useful research lead, but the observed 60% holdout accuracy is not sufficient evidence of directional predictability after accounting for model search and the small 20-event holdout. No premium-only combination is promoted to trading.

### Phase 5 next gate
1. Freeze the two call-wing ratio candidates before further testing.
2. Run rolling/expanding chronological validation.
3. Test alternative 10:00 timestamp semantics as a robustness analysis without changing the primary convention.
4. Split by volatility/trend/expiry-week/event regimes and liquidity/volume/OI availability.
5. Replicate on the independent secondary source for the same eligible events.
6. Apply placebos/permutation tests and report multiple-testing corrections before any economic/trading translation.


## 2026-10-02 — Phase 5 frozen-candidate robustness

The two pre-specified call-wing ratio candidates (CE OTM6/OTM7 and CE OTM6/OTM8 log-ratios) were frozen and evaluated without holdout threshold tuning.

- Both candidates: 59.41% development accuracy and 60.0% (12/20) on the 2026 holdout.
- Both candidates produce identical classifications on the 2026 holdout: 3 bullish and 17 bearish.
- Expanding walk-forward accuracy: 63.37% for CE OTM6/OTM7 and 62.38% for CE OTM6/OTM8; these p-values are unadjusted exploratory statistics.
- Pre-September-2025 accuracy: 62.35%; post-September-2025 accuracy: 52.78%.
- 2026 exact binomial p=0.5034; the always-bearish holdout baseline is 65%.

The apparent historical walk-forward signal therefore deteriorates around the expiry-convention regime boundary and does not improve the final holdout baseline. Continue Phase 5 only with independent-source replication, liquidity/quote robustness, timestamp sensitivity, and placebo/multiple-testing controls. No trading translation.


### Single-premium result
The six raw premiums were also screened individually using development-only median thresholds with both directional mappings. On the 2026 holdout, the call premiums reached 55% (11/20) under their better mapping, while the put premiums reached 50% (10/20). Therefore no individual premium is supported as a standalone direction predictor.
