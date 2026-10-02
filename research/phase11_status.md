# Phase 11 Status — NIFTY Spot-Based Stop-Loss

State: **PARTITIONING CORRECTED / RE-RUN QUEUED**

Branch: `phase-11-nifty-spot-stop`

## Frozen question
Can NIFTY spot movement define a useful stop-loss trigger for the Phase 9 strategy independently of option premium/P&L?

## Status
- 11.1 Plan and branch: COMPLETED
- 11.2 Data audit: COMPLETED
- 11.3 Candidate grid: FROZEN; prior run cancelled before acceptance
- 11.4 Validation selection: INVALIDATED — expiry/entry partition mismatch
- 11.5 Untouched test: INVALIDATED — expiry/entry partition mismatch
- 11.6 Synthesis and closure: PENDING

No Phase 11 numerical result has been accepted. The previous candidate-grid summary was invalidated because split membership used entry dates instead of the expiry-date keys in the frozen Phase 9 metadata. A directional-sign error was corrected before the rerun.


## Latest execution audit — 2026-10-02
- Run 37028523476 failed after approximately 24 minutes in the validation/test partitioning stage.
- Unit tests passed (4/4); no numerical output was accepted or committed.
- Root cause was candidate variable val shadowing the validation-date set. Corrected in commit f797baefe597969d2241971f6ea15095a92d911a.
- A new workflow run is expected from the correction commit. Acceptance remains gated on successful completion, persisted outputs, and remote readback.


## Latest execution correction — 2026-10-02
- Run 37031544256 completed successfully but produced invalid partition metrics: all validation/test counts were zero despite each raw candidate run containing 56 trades.
- Root cause: split metadata dates represent expiry dates; the Phase 11 engine used entry dates for `isin()` partitioning.
- Corrected in commit 471c81d6a7cdf3f07db30646d7593a298b05dfea.
- No numerical result from the invalid partition was accepted. Re-run acceptance requires nonzero validation/test counts, persisted outputs, and remote readback.
