# Phase 11 Research Plan — NIFTY OTM7+OTM8−OTM6 Premium Direction Predictor

## 0. Research question and hypothesis

### Primary research question
At the 4-trading-day-to-expiry observation point, can the relative option-premium measure

- **Call score:** C(OTM7) + C(OTM8) − C(OTM6)
- **Put score:** P(OTM7) + P(OTM8) − P(OTM6)
- **Spread:** Call score − Put score

predict the direction of the NIFTY 50 from the observation spot to that weekly expiry?

### Primary directional rule supplied by the user
- If **Call score > Put score**, classify the future NIFTY direction as **BEARISH**.
- If **Put score > Call score**, classify the future NIFTY direction as **BULLISH**.
- If scores are equal, classify as **NEUTRAL / TIE** and report separately rather than forcing a direction.

The primary analysis will preserve this rule exactly. A separate diagnostic will test the inverse mapping only as a label-consistency check; it will not replace the primary hypothesis.

### Primary horizon
From the NIFTY spot at the observation timestamp to the NIFTY expiry settlement value for the same weekly contract.

### Observation timestamp
Use **10:00 Asia/Kolkata** on the trading day that is exactly 4 trading sessions before expiry, inheriting the project's established 4-DTE/10:00 convention unless the protocol is explicitly revised and logged.

---

## 1. Phase 0 — Protocol freeze

1. Freeze the formula and directional mapping.
2. Freeze the 4-trading-day definition using the exchange trading calendar, not a calendar-day approximation.
3. Freeze the observation time at 10:00 IST.
4. Define OTM6/OTM7/OTM8 from the contemporaneous NIFTY spot and the applicable NIFTY strike grid.
5. Define premium source hierarchy:
   1. executable bid/ask where reliable,
   2. otherwise trade/quote-derived price at the timestamp,
   3. midpoint only as a sensitivity analysis,
   4. never silently substitute an unrelated strike or expiry.
6. Freeze handling of missing/illiquid contracts, stale quotes, zero volume, and crossed/invalid quotes.
7. Freeze the target label as sign of expiry value minus observation spot; exact ties are neutral.
8. Freeze the primary statistical analysis before inspecting final outcomes.

**Exit criterion:** specification is internally consistent and versioned.

---

## 2. Phase 1 — Historical data acquisition and validation

### Required data
For each weekly NIFTY expiry in the sample:

- NIFTY spot/index value at 10:00 IST on 4-DTE session.
- Exact weekly expiry date.
- Applicable strike interval/strike master for that date.
- Six option observations at the target expiry:
  - OTM6 CE, OTM7 CE, OTM8 CE
  - OTM6 PE, OTM7 PE, OTM8 PE
- Quote/trade timestamp and source.
- Bid, ask, last traded price, volume, open interest when available.
- NIFTY expiry settlement/official expiry value.
- Trading-calendar and holiday metadata.
- Data-source provenance and retrieval timestamp.

### Strike convention
OTM levels are determined from the contemporaneous spot and exchange strike grid. The implementation must explicitly document how ATM is selected when spot is between strikes and how OTM6/7/8 are counted from ATM.

### Source strategy
Search and cross-check, in descending preference:

1. NSE official contract/market archives.
2. BSE where an equivalent required record is available.
3. Open-source historical market-data repositories.
4. GitHub datasets/ETL projects.
5. Kaggle.
6. Hugging Face datasets using the repository's HF_TOKEN secret.
7. Other reputable historical-data providers when legally and technically accessible.

Important data will be cached in the repository's data-cache mechanism or equivalent release artifact; workflows must not re-download the full history on every run.

### Validation
- Expiry/date consistency.
- No duplicate contract/timestamp rows.
- Correct option type and expiry.
- Correct strike and moneyness.
- Plausible bid/ask relationship.
- Timestamp nearest to, but not silently after, 10:00.
- Cross-source spot checks.
- Contract lot/strike specification checks.
- Identification of structural breaks in expiry conventions.

**Critical calendar break:** NSE revised NIFTY weekly expiry from Thursday to Tuesday for new contracts expiring from September 2025 onward. The research must therefore make expiry-calendar logic date-aware and split robustness tests around this regime change.

**Exit criterion:** a reproducible, validated event-level dataset exists and its coverage is documented.

---

## 3. Phase 2 — Feature engineering

For each event:

- Call score = CE7 + CE8 − CE6.
- Put score = PE7 + PE8 − PE6.
- Premium spread = Call score − Put score.
- Relative spread = Premium spread / (|Call score| + |Put score|) when denominator > 0.
- Call/put score ratio where defined.
- Signed signal under the user's rule.
- Entry spot.
- Expiry settlement.
- Return to expiry = (expiry settlement / entry spot) − 1.
- Point move = expiry settlement − entry spot.
- Direction label = bullish / bearish / neutral.

Secondary controls, where data permits:
- NIFTY India VIX at observation.
- Distance to ATM / realized moneyness.
- Aggregate option IVs.
- Put-call premium ratios.
- Open interest and volume summaries.
- Market-regime variables.
- Overnight/global-market context.

The predictor must be computed from option information available at the observation timestamp only.

---

## 4. Phase 3 — Primary directional test

### Primary test
Measure whether the user's mapping predicts the sign of the subsequent NIFTY move.

Report:
- Number of bullish, bearish, and neutral predictions.
- Correct/incorrect classifications.
- Accuracy excluding neutral cases.
- Accuracy including neutral cases under a pre-specified tie policy.
- Confusion matrix.
- Precision/recall for each direction.
- Balanced accuracy.
- 95% confidence intervals.

### Statistical significance
Use:
- Exact binomial test against the appropriate null for binary directional classification.
- Bootstrap confidence interval for accuracy and mean expiry return by predicted direction.
- Association tests between signal buckets and realized direction.
- Correlation between continuous premium spread and future NIFTY return.
- Logistic regression using the continuous spread as the primary predictor.

The regression coefficient and confidence interval must be reported; no significance claim will be based on a single metric.

---

## 5. Phase 4 — Out-of-sample and multiple-testing protection

The sample will be split chronologically into development and holdout periods.

Primary rule is frozen before holdout evaluation.

Tests:
1. In-sample descriptive results.
2. Walk-forward or rolling-origin validation where sample length permits.
3. Final untouched holdout.
4. Bootstrap by expiry blocks, not individual observations, where serial dependence could matter.

No signal threshold will be tuned on the final holdout.

---

## 6. Phase 5 — Robustness and falsification

### Execution/measurement robustness
- Bid/ask midpoint vs conservative executable-side prices.
- Small slippage assumptions.
- Nearest quote within a documented timestamp tolerance.
- Alternative treatment of stale/illiquid quotes.
- Excluding observations with poor liquidity.

### Economic robustness
- Pre/post September 2025 expiry-convention split.
- High/low India VIX regimes.
- Large/small absolute NIFTY moves.
- Bull/bear/sideways market regimes.
- Monthly/quarterly expiry contamination checks.
- Holiday-shortened weeks.
- Strike-grid changes.

### Falsification
- Inverse directional mapping as a diagnostic.
- Randomized/permuted signal labels.
- Placebo timestamps when data permits.
- Compare against simple baselines:
  - always-bullish,
  - always-bearish,
  - previous-session direction,
  - basic call-put premium difference.

A predictor that only works for one arbitrary mapping, one data source, or one narrow regime will not be treated as robust.

---

## 7. Phase 6 — Trading translation, only after predictive validity

If and only if the directional predictor demonstrates statistically and economically credible out-of-sample information:

- Define a simple directional NIFTY implementation.
- Account for Paytm Money brokerage and all applicable statutory/exchange charges.
- Include bid/ask and slippage.
- Use actual historical contract/lot-size rules.
- Report gross and net returns, turnover, drawdown, hit rate, expectancy, and cost sensitivity.
- Do not optimize a trading threshold on the final holdout.

This phase is secondary to the research question and must not contaminate the primary predictor test.

---

## 8. Phase 7 — Manuscript and research package

Produce a complete research manuscript containing:

1. Abstract
2. Introduction
3. Research questions and hypotheses
4. Literature review
5. Data and provenance
6. Methodology
7. Statistical analysis plan
8. Results
9. Robustness tests
10. Discussion
11. Strengths
12. Limitations
13. Conclusion
14. Future research
15. References
16. Appendices
17. Data dictionary
18. Reproducibility instructions
19. Supplementary tables/charts

Required visuals:
- Distribution of premium spread.
- Spread vs subsequent return.
- Hit-rate by signal decile.
- Calibration/conditional-direction chart.
- Regime-split results.
- Confusion matrix.
- Cumulative hypothetical directional P&L only if Phase 6 is justified.

---

## 9. Research completion rule

The research stops after the defined phases above. It should conclude with one of:

- credible evidence that the predictor contains directional information,
- evidence that the observed relationship is statistically weak/unstable,
- or an inconclusive result caused by insufficient/low-quality historical data.

The final conclusion must distinguish statistical significance, economic significance, and data-quality limitations.

