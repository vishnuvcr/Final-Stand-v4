# Error Log

## 2026-10-01
- No research-code error yet.
- Repository was initially empty; baseline research files were initialized during strategy-specification setup.
- A previous interpretation used a fixed OTM8 → OTM12 → OTM16 roll. This is superseded by V2: re-calculate OTM8 from the current spot after each trigger.

## Phase 1 infrastructure errors — 2026-10-01
- GitHub Actions runs initially failed because the cache key contained a comma from the YEARS input. Fixed by removing YEARS from the cache key.
- The current Phase 1 backtest run passed dependency installation and all unit tests, then remained in the data-processing step for an extended period. This is recorded as a performance/observability issue; no research result is accepted until the run completes.
- The interactive tool session timed out while waiting for the long-running GitHub Actions job. This does not imply a backtest failure.
