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
