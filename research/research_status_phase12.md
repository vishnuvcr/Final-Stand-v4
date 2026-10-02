# Phase 12 Research Status

**Branch:** phase-12-full-chain-oi-direction  
**Status:** Workflow hardened after a failed Actions run; empirical full-chain extraction/model run is pending a successful GitHub Actions execution.  
**Last updated:** 2026-10-02

## Scope
This phase expands the prior six-premium search to **all available NIFTY strikes at 4-DTE/10:00 IST**, including option premium, open interest and volume surfaces.

## Phase status
| Phase | Status |
|---|---|
| 0 — Scope/protocol expansion | COMPLETE |
| 1 — Full-chain extraction | CODE COMPLETE; EXECUTION PENDING |
| 2 — Feature engineering | CODE COMPLETE |
| 3 — Model screening | CODE COMPLETE |
| 4 — Holdout/multiple-testing | CODE COMPLETE |
| 5 — Independent replication/robustness | NOT STARTED |
| 6 — Trading translation | NOT STARTED |
| 7 — Manuscript | NOT STARTED |

## Frozen protocol
- 4 trading sessions before weekly expiry.
- 10:00:00 IST one-minute bar OPEN.
- All available strikes for the target expiry.
- CE/PE premium, OI and volume where present.
- ATM-relative strike-distance representation.
- No forward filling/interpolation across missing strikes.
- Development: expiries before 2026.
- Holdout: expiries in 2026.
- Model selection only on development.
- Multiple-testing permutation diagnostic.
- No trading translation without robust holdout evidence.

## Current gate
The previous Actions attempt failed, as shown in the user's GitHub Actions screenshot, before any empirical Phase 12 result became available through the repository connector. The exact failed step was not observable through the connector.

The workflow has now been hardened to remove in-run execution-marker pushes and to upload install/acquisition/extraction/analysis logs even when the run fails. The next successful run is the gate for empirical analysis.

## Next gate
Run/observe the hardened Phase 12 workflow. Inspect the generated artifact and/or committed result files before proceeding. Required checks: available strikes per event, exact 10:00 coverage, OI/volume missingness, selected development model, 2026 holdout balanced accuracy/MCC, and permutation p-value.

Then either proceed to independent replication or close the phase as negative/inconclusive. No further unconstrained feature mining is planned.

## Current execution update
Run 37009066361: acquisition SUCCESS; extraction SUCCESS; model analysis IN PROGRESS; publication PENDING. The current analysis includes the pre-specified development screening and 500-permutation multiple-testing diagnostic. No empirical performance figure is accepted until completion.
