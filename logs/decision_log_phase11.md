# Decision / Conversation Log — Phase 11

## 2026-10-02 — New research requested

User requested a separate research branch to test whether the following 4-DTE NIFTY option premium construction can predict the direction from the observation spot to weekly expiry:

- Call calculation = OTM7 call premium + OTM8 call premium − OTM6 call premium.
- Put calculation = OTM7 put premium + OTM8 put premium − OTM6 put premium.
- If call calculation > put calculation → predict bearish.
- If put calculation > call calculation → predict bullish.

### Decisions recorded

1. New branch: `phase-11-premium-direction-predictor`.
2. Primary formula and directional mapping are frozen exactly as supplied.
3. Observation timestamp inherits the project's established 4-DTE / 10:00 IST convention.
4. Outcome is NIFTY expiry settlement versus the 10:00 entry spot.
5. Equality is a neutral/tie observation, not forced into either direction.
6. The primary study is predictive/statistical first; a trading implementation is a later phase.
7. Historical expiry-calendar rules are date-aware. NSE revised NIFTY weekly expiry from Thursday to Tuesday for new contracts from September 2025 onward.
8. Cost modelling must include slippage and applicable Paytm Money brokerage/statutory/exchange charges if a trading implementation is reached.
9. The inverse label mapping will be tested only as a diagnostic, not silently substituted for the user's primary rule.

Hidden chain-of-thought is not stored. This log stores requirements and implementation decisions.


## 2026-10-02 — Phase 1/2 protocol decisions

1. **Primary 10:00 price:** use the 10:00:00 one-minute bar OPEN for options and NIFTY spot to prevent look-ahead from the rest of the 10:00 minute.
2. **Four-DTE definition:** fourth distinct prior NIFTY trading session before each expiry.
3. **Expiry outcome:** use the latest 1-minute NIFTY CLOSE on the expiry session as a provisional settlement proxy, pending official NSE settlement validation.
4. **Missing-data treatment:** exact 10:00 snapshots are required for the six option legs and spot. No silent forward fill.
5. **Event construction:** nearest listed strike to the 10:00 spot is used as ATM; the observed strike interval is inferred from the contemporaneous strike grid, and OTM6/7/8 are six/seven/eight intervals away on the appropriate side.
6. **Research source plan:** cache candidate NIFTY option Parquet data from the identified Hugging Face dataset and NIFTY spot 1-minute files from the identified open GitHub dataset; cross-check selected events using an independent source before final claims.


## 2026-10-02 — Implementation checkpoint

- Added signal calculator, event-builder, helper tests, and cached acquisition script.
- Added manual workflow actions: validate, acquire, build.
- Derived event data will be committed to `results/phase11_events.csv` and JSON coverage report when the build action is executed successfully.


## 2026-10-02 — Acquisition gate decision

The Phase 11 primary hypothesis requires point-in-time 10:00 option premiums. EOD option archives cannot answer it. Therefore no EOD-derived proxy, synthetic reconstruction, or unrelated prior backtest result will be used as a substitute. The research remains at the Phase 1 gate until the specified intraday data can actually be acquired and validated.


## 2026-10-02 — Primary data-source decision

TradeMarkk's `thetrademarkk/india-index-options-1m` is adopted as the current primary candidate because it exposes expiry-partitioned NIFTY 1-minute Parquet files plus a NIFTY 1-minute spot file, with IST timestamps and OHLCV+OI. Its documentation explicitly warns that far/illiquid strike coverage can be sparse. This is therefore a provisional source selection pending empirical coverage and cross-source price validation.

The Rissin `nse-options-intraday` Upstox-derived archive is retained as an independent secondary source. OptionsData.shop, MoneyTicks, Shoonya/Cloud Trader Pro, Unfluke, Breeze, NSE, TrueData and GDFL remain documented alternatives.

The primary event builder must use the TradeMarkk source without silently substituting the secondary source. Cross-source agreement will be assessed separately.


## 2026-10-02 — Phase 3/4 decision

The primary directional hypothesis is not promoted to trading translation at this stage.

Evidence:
- 61/121 correct = 50.41%.
- Exact binomial p = 1.000 against the 50% null.
- 2026 chronological holdout = 9/20 = 45.0%.
- Overall Pearson spread/expiry-return r = -0.2086 (p=0.02165), but Spearman rho = -0.1118 (p=0.22223), logistic slope p=0.22877, and 2026 holdout Pearson p=0.8154.
- Independent source audit: 81/82 eligible overlapping events matched, with all six legs present for all matched events and mean relative price difference 0.3045%.

Decision: treat the Pearson relationship as exploratory/non-robust. Continue to Phase 5 robustness/falsification; do not construct a live or historical trading strategy from this predictor yet.
