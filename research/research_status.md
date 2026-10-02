# Research Status

## Phase 0 — Strategy specification
**Status: COMPLETED**

### Completed
- Captured Strategy V2 initial legs.
- Changed dynamic adjustment rule from fixed OTM12-style rolling to current-spot OTM8 re-centering.
- Documented the supplied screenshot mapping.
- Identified the key implementation ambiguity: exact OTM strike-selection convention when current spot is between strikes.

### Pending
- Extend validation beyond the current candidate sample.
- Validate exact execution-cost schedule against historical Paytm Money/NSE/SEBI rates.
- Add intrabar high/low trigger sensitivity.

## Phase transition rule
Phase 1 should begin only after the specification and execution conventions are frozen.


## Phase 0 research evidence update — 2026-10-01
- NSE's current NIFTY 50 specification states 50-point strike intervals for weekly/monthly index options and Tuesday expiry under the current regime. See NSE source cited in the research report.
- NSE exposes contract-wise derivatives price/volume archives and documents historical F&O bhavcopy structure.
- A public Hugging Face dataset was identified containing NIFTY 1-minute options from Oct 2024 onward plus long EOD history. It is a candidate source and must be validated against NSE records.
- Public GitHub projects document alternative NIFTY 1-minute option pipelines/datasets. They are secondary/validation sources, not automatically ground truth.

### Phase 0 conclusion
The specification is implementable. The backtest will use the actual historical expiry calendar and strike availability rather than assuming today's rules across all years. Historical expiry/strike regimes must be versioned by date.

### Phase 1 status
**READY TO START — data acquisition + validation.**

## Phase 1 execution checkpoint — 2026-10-01
- Unit tests: **PASSED** in GitHub Actions.
- Data/backtest job: **RUNNING / NOT YET ACCEPTED** at checkpoint.
- No performance conclusion is reported until the data-processing run completes and outputs are validated.
- Current run: GitHub Actions run 36837298146.


## Phase 1 remediation checkpoint — 2026-10-01
- Exchange validation updated: current NIFTY weekly/monthly strike interval is 50 points; Tuesday expiry with previous-trading-day holiday adjustment.
- Historical NIFTY lot-size treatment added: 75 through 30-Dec-2025 expiry; 65 thereafter.
- Backtest engine optimized to read only expiry/strike windows required by the strategy instead of materializing the entire option history.
- Unit tests remain passed; performance-optimized backtest execution is in progress.


## Phase 1 run — [2025, 2026]
- Status: **EXECUTED IN GITHUB ACTIONS**
- Option rows processed: None
- Spot rows processed: None
- Expiries discovered: None
- Trades produced: 77
- Skips: 99


## Phase 1 data-quality correction — 2026-10-01
- The first completed optimized run is **REJECTED for analysis** because its candidate-strike filter used the 09:15 spot for initial strike availability while the strategy entry is defined at 10:00.
- Engine correction applied: initial candidate strikes are now derived from the actual 10:00 spot; dynamic OTM8 candidates continue to be derived from all observed spot closes in the holding window.
- The 77-trade result set is therefore provisional and must not be interpreted as a research result. A corrected run is required.


## Phase 1 run — [2025, 2026]
- Status: **EXECUTED IN GITHUB ACTIONS**
- Option rows processed: None
- Spot rows processed: None
- Expiries discovered: None
- Trades produced: 84
- Skips: 92


## Phase 1 run — [2025, 2026]
- Status: **EXECUTED IN GITHUB ACTIONS**
- Option rows processed: None
- Spot rows processed: None
- Expiries discovered: None
- Trades produced: 84
- Skips: 92


## Corrected Phase 1 result — 2026-10-01
- GitHub Actions corrected run: **SUCCESS**.
- Unit tests: **PASSED**.
- Statistical analysis: **PASSED**.
- Empirical sample actually represented by the available validated option data: **84 trades (42 CE, 42 PE)**, not all 2025–2026 expiries.
- Major coverage gap: many 2025 expiries before September are unavailable in the selected intraday option dataset; these are recorded as skips and are not imputed.
- Lot size is modeled as 75 through the 30-Dec-2025 expiry and 65 thereafter, consistent with the NSE lot-size revision. See NSE circular source in the manuscript/data-source register.
- Target exit is modeled at the next available minute after the target is observed, avoiding same-bar look-ahead.

### Preliminary descriptive result — not final robustness conclusion
- CE: 42 trades; 92.86% target-hit; mean net P&L ₹282.38; median ₹356.88; total ₹11,860; profit factor 1.48.
- PE: 42 trades; 78.57% target-hit; mean net P&L -₹1,131.67; median ₹335.62; total -₹47,530.15; profit factor 0.40.
- Aligned CE-vs-PE permutation test p=0.1449; Mann–Whitney p=0.6514. These are descriptive, not a basis for a trading recommendation.
- Bootstrap 95% CI for mean net P&L: CE approximately ₹-858 to ₹1,121; PE approximately ₹-2,732 to ₹259.

### Phase 1 conclusion
The initial sample shows materially different observed aggregate P&L and tail-loss behavior between the two variants, but the sample is incomplete and the uncertainty intervals are wide. The result is therefore **not sufficient for a final research conclusion**. Phase 2 must validate trigger/expiry mechanics and Phase 3 must run the predefined robustness grid.

### Phase 2 status
**READY TO START — engine validation and synthetic-path tests.**

## Phase 3 robustness grid execution
- Target fractions: 90%, 95%, 100% of initial flatline.
- Slippage: 0.00, 0.10, 0.25 option-premium points per execution.
- Brokerage: ₹20 per executed order.
- All scenarios use the validated current-spot OTM8 re-centering logic.

## Phase 4 statistical analysis — baseline scenario
- Target: 100% of initial flatline.
- Slippage: 0.10 premium points per execution.
- Brokerage: ₹20 per executed order.
- Statistical outputs generated from the corrected trade ledger.


## Phase 4 completion — 2026-10-01
- GitHub Actions run 36842315280: **SUCCESS**.
- Baseline statistical outputs regenerated after the explicit transaction-cost model was implemented.
- Baseline CE: 42 trades; mean net P&L ₹190.35; median ₹271.06; total ₹7,994.79; profit factor 1.31; 71.43% profitable trades.
- Baseline PE: 42 trades; mean net P&L -₹1,230.55; median ₹250.50; total -₹51,683.26; profit factor 0.36; 78.57% profitable trades.
- Bootstrap 95% CI for mean net P&L: CE approximately ₹-956 to ₹1,030; PE approximately ₹-2,840 to ₹166.
- CE-vs-PE tests: Mann–Whitney p=0.6579; paired sign-permutation p=0.1443. These do not establish a statistically significant difference at conventional thresholds.
- Phase 3 robustness grid completed successfully. Across the tested target/slippage scenarios, aggregate CE net P&L remained positive while aggregate PE net P&L remained negative; this is an observed sample result, not a claim of future performance.

## Phase 5 status
**COMPLETED — manuscript synthesis, figures, limitations, and final research conclusion.**


## Final research checkpoint — 2026-10-01
- Phase 5 GitHub Actions run 36842855381: **SUCCESS**.
- Date-aware NSE transaction charges and STT were incorporated before the final baseline rerun.
- Final baseline: CE mean net ₹189.35, total ₹7,952.82; PE mean net -₹1,231.88, total -₹51,739.07.
- CE/PE tests: Mann–Whitney p=0.6579; paired sign-permutation p=0.1444.
- Final manuscript created at manuscript/final_research_manuscript.md.
- Research stopping rule reached: all proposed computational phases completed; remaining items are explicitly listed as future research rather than open-ended continuation.


## Phase 6 — Strategy V3 restart — 2026-10-01
- Status: **COMPLETED**.
- New strategy replaces the V2 profit-target/recentering rules for this research phase; V2 files remain frozen as the prior baseline.
- Required tests: unit tests, full 2025–2026 backtest, call/put comparison, descriptive CE/PE ratios, statistical tests, and transaction-cost accounting.
- Trigger: initial OTM8 breach using one-minute high/low; execution on the next minute open.
- Roll: one-time replacement of the short initial OTM8 option with the opposite option at the same initial OTM8 strike.
- Exit: 0 DTE, 15:29 bar open.


## Phase 6 — Strategy V3 static OTM8 reversal — execution checkpoint
- Status: **EXECUTED IN GITHUB ACTIONS**
- Strategy: static initial OTM8 trigger; one-time replacement of short OTM8 with opposite option at the same initial OTM8 strike.
- Exit: 0 DTE, 15:29 bar open.
- Trades produced: 84
- Skips: 92
- Full data-quality record: results/strategy_v3_data_quality.json


## Phase 6 — Strategy V3 final checkpoint — 2026-10-01
- Status: **COMPLETED**.
- Latest successful workflow run produced 84 trades: 42 CE and 42 PE; 92 trade-side skips are documented rather than imputed.
- Strategy 1 Put: total net ₹-58,006.84; mean ₹-1,381.12; median ₹397.00; win rate 83.33%; profit factor 0.502; worst trade ₹-56,338.09; roll rate 21.43%.
- Strategy 2 Call: total net ₹29,527.08; mean ₹703.03; median ₹291.08; win rate 69.05%; profit factor 2.715; worst trade ₹-9,757.58; roll rate 9.52%.
- CE/PE aligned tests: Mann–Whitney p=0.9893; paired sign-permutation p=0.2704. These do not establish a statistically significant difference.
- 95% bootstrap mean intervals: CE approximately ₹-116 to ₹1,450; PE approximately ₹-4,699 to ₹1,199.
- Expiry-only exit was used; no profit target or dynamic re-centering was used.
- The prior V2 baseline remains frozen and is not overwritten by V3.


## Phase 6 — Strategy V3 static OTM8 reversal — execution checkpoint
- Status: **EXECUTED IN GITHUB ACTIONS**
- Strategy: static initial OTM8 trigger; one-time replacement of short OTM8 with opposite option at the same initial OTM8 strike.
- Exit: 0 DTE, 15:29 bar open.
- Trades produced: 84
- Skips: 92
- Full data-quality record: results/strategy_v3_data_quality.json


## Phase 9 — Credit-Selected OTM6/7/8 — 2026-10-02
- Status: **IN PROGRESS — specification and implementation committed; empirical run pending**.
- User rule implemented: compare `PE7 + PE8 - PE6` with `CE7 + CE8 - CE6` at 10:00 and select the higher positive credit.
- Primary exit target frozen at 90% of the entry flatline after entry slippage.
- Stop-loss candidates frozen before the run; one stop will be selected on the validation segment only.
- Expiry identification now uses the historical contract expiry field and nearest-expiry test rather than assuming Tuesday across all 2025–2026 observations.
- Primary costs use Paytm Money ₹10/order plus exchange, SEBI, stamp duty, STT, GST and 0.10-point adverse slippage.
- No dynamic OTM8 re-centering or reversal is carried forward from V2/V3.
