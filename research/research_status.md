# Research Status

## Phase 0 — Strategy specification
**Status: IN PROGRESS**

### Completed
- Captured Strategy V2 initial legs.
- Changed dynamic adjustment rule from fixed OTM12-style rolling to current-spot OTM8 re-centering.
- Documented the supplied screenshot mapping.
- Identified the key implementation ambiguity: exact OTM strike-selection convention when current spot is between strikes.

### Pending
- Confirm exact strike-selection convention.
- Acquire/validate historical NIFTY spot and option-chain data.
- Define executable timestamp/price model and costs.
- Implement backtest and validation tests.

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
