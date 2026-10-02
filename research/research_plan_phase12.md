# Phase 12 Research Plan — Full NIFTY Option Surface, Open Interest and Volume Direction Predictor

## Research question

Can the complete NIFTY option surface available at 4 trading days before weekly expiry and 10:00 IST contain directional information about the NIFTY move from the observation spot to expiry, beyond the six pre-selected OTM6/7/8 premiums?

## Scope expansion

This phase explicitly removes the OTM6/7/8 restriction. For every eligible event, use **all available strikes** for the target weekly expiry at the exact 10:00 IST observation.

Variables to inspect, where present:
- CE and PE OHLC prices;
- open interest;
- change in open interest when derivable;
- traded volume;
- strike and moneyness;
- call/put OI and premium distributions across the entire strike surface;
- ATM-relative option-surface shape;
- OI concentration and imbalance;
- premium-weighted and OI-weighted strike moments;
- put-call ratios;
- max-OI / max-premium strike locations;
- call-wing and put-wing slopes/curvature;
- total-chain and near-ATM subsets;
- broad-wing and tail subsets.

No feature is allowed to use information after 10:00 IST.

## Phase 0 — Protocol expansion

1. Preserve the existing 4-DTE and 10:00:00 IST-open convention.
2. Preserve the existing expiry outcome definition pending official historical settlement validation.
3. Freeze all-strike extraction before model evaluation.
4. Encode strikes relative to the contemporaneous ATM and strike interval.
5. Do not infer missing far-strike values by forward filling.
6. Distinguish absent/illiquid strikes from zero-valued premiums or OI.
7. Keep 2026 as the untouched chronological holdout.
8. Prevent feature selection from using holdout observations.

## Phase 1 — Full-chain data extraction

For each of the 121 existing valid events:
- load the primary TradeMarkk expiry parquet;
- select the exact 10:00:00 IST observation;
- retain every available strike for the event's expiry;
- retain CE/PE price, OI and volume;
- audit strike continuity, duplicates and missing fields;
- generate a compact event-level feature table rather than committing the full raw archive.

The TradeMarkk dataset documents 1-minute OHLCV(+OI) NIFTY option-chain data and explicitly notes that far/illiquid strikes can be sparse. The OptionsData.shop archive is an independent full-chain candidate advertising every strike/expiry with OI and 1-minute OHLCV; it is a secondary source candidate, not an assumed source of truth.

## Phase 2 — Feature families

### A. Full-surface strike vectors
Create ATM-relative vectors for CE and PE premium, OI and volume at strike distances where data exists, with explicit missingness indicators.

### B. Aggregate chain metrics
Compute:
- total CE OI / total PE OI;
- OI PCR;
- total CE volume / PE volume;
- volume PCR;
- total premium by side;
- premium PCR;
- OI-weighted mean strike;
- OI-weighted strike dispersion;
- volume-weighted strike moments;
- premium-weighted strike moments;
- call-vs-put OI imbalance;
- call-vs-put volume imbalance.

### C. Concentration / positioning
Compute:
- maximum CE OI strike and distance from ATM;
- maximum PE OI strike and distance from ATM;
- concentration ratios;
- OI shares in near-ATM, medium-wing and far-wing bands;
- OI asymmetry by distance from ATM.

### D. Surface shape
Compute finite-difference slopes and curvature of call/put premium and OI curves around ATM and across wings.

### E. Traditional option-chain structures
Where mathematically defined:
- PCR variants;
- OI-weighted PCR;
- max-pain-style strike measures;
- call/put OI walls;
- distance between major call and put OI concentrations;
- skew proxies from call/put relative premium shapes.

### F. Regime/context controls
Join only information available by 10:00:
- NIFTY return from prior close;
- overnight/global proxy where reliably available;
- India VIX if available;
- futures basis/OI if available;
- expiry-week/calendar regime.

## Phase 3 — Model protocol

Primary development period: expiry before 2026-01-01.
Final chronological holdout: expiry on/after 2026-01-01.

Models:
1. regularized logistic regression;
2. shallow tree/ensemble benchmark;
3. simple feature-family scores;
4. direction-neutral baseline.

Feature scaling is fitted on development folds only.

Development model selection:
- chronological/blocked cross-validation;
- no holdout tuning;
- limit model complexity because the event sample is only 121 observations.

Report:
- accuracy;
- balanced accuracy;
- MCC;
- confusion matrix;
- ROC-AUC where probabilities are available;
- bootstrap confidence intervals;
- exact binomial diagnostics where appropriate.

## Phase 4 — Multiple-testing / falsification

Because full-chain feature mining creates a large search space:
- report the number of candidate features/families/models;
- use permutation of development labels to estimate the distribution of the best development score under no signal;
- keep 2026 completely untouched;
- require improvement over class-frequency and balanced baselines;
- repeat the final candidate on the independent source where possible.

A candidate found only after extensive search is a research lead, not a validated predictor.

## Phase 5 — Cross-source and measurement robustness

1. Replicate selected features on the independent Rissin/Upstox archive where OI is available.
2. Compare primary vs secondary premium measurements.
3. Test whether the signal survives reasonable timestamp/quote treatment.
4. Split around the September 2025 NIFTY expiry-convention change.
5. Test liquidity/coverage filters.
6. Test high/low volatility and trend regimes.

## Phase 6 — Economic translation gate

No options trading strategy is constructed unless the predictor passes:
- chronological holdout;
- multiple-testing control;
- independent-source replication;
- measurement robustness.

If it passes, only then model Paytm Money brokerage, exchange/statutory charges, bid/ask, slippage, lot-size changes and turnover.

## Phase 7 — Final manuscript

Update the Phase 11/12 manuscript package with:
- feature-family tables;
- full-chain visualizations;
- OI/premium surface plots;
- model comparison;
- holdout confusion matrices;
- permutation distributions;
- cross-source replication;
- limitations and future research.

## Stop rule

Stop after this defined full-chain protocol. Do not expand indefinitely into arbitrary feature mining. If no robust signal survives, close the research question with a documented negative/inconclusive conclusion.
