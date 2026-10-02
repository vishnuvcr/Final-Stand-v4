# Phase 11 Research Status

**Branch:** phase-11-premium-direction-predictor  
**Status:** Phase 0 — protocol initialized; literature review started; data acquisition not yet run.  
**Last updated:** 2026-10-02

## Phase status

| Phase | Status |
|---|---|
| 0 — Protocol freeze | IN PROGRESS |
| 1 — Data acquisition/validation | NOT STARTED |
| 2 — Feature engineering | NOT STARTED |
| 3 — Primary directional test | NOT STARTED |
| 4 — Out-of-sample validation | NOT STARTED |
| 5 — Robustness/falsification | NOT STARTED |
| 6 — Trading translation | NOT STARTED |
| 7 — Manuscript/conclusion | NOT STARTED |

## Completed in this branch

- Created a separate Phase 11 branch from main.
- Recorded the user's predictor formula and exact directional mapping.
- Preserved the project's 4-DTE / 10:00 IST convention.
- Defined the outcome as movement from the 10:00 spot to expiry settlement.
- Added a date-aware plan for the NSE Thursday-to-Tuesday expiry regime change.
- Defined the primary statistics and robustness framework.
- Identified Paytm Money execution-cost treatment as a secondary trading-translation phase.

## Latest execution note

- Initial workflow registration produced an immediate GitHub Actions failure with no exposed job details. The workflow was simplified to manual-run validation only; this is logged and does not affect research results.

## Current blockers

Historical 10:00 IST option observations with reliable strike-level bid/ask/trade data must be acquired and validated before any performance conclusion is drawn.

## Next execution gate

Phase 0 exits only after the data schema, strike-selection function, timestamp tolerance, missing-data policy, and primary statistical protocol are implemented and tested.
