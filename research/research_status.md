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
