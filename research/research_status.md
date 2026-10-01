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
