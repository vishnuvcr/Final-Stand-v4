# Error Log

## 2026-10-01
- No research-code error yet.
- Repository was initially empty; baseline research files were initialized during strategy-specification setup.
- A previous interpretation used a fixed OTM8 → OTM12 → OTM16 roll. This is superseded by V2: re-calculate OTM8 from the current spot after each trigger.

## Phase 1 infrastructure errors — 2026-10-01
- GitHub Actions runs initially failed because the cache key contained a comma from the YEARS input. Fixed by removing YEARS from the cache key.
- The current Phase 1 backtest run passed dependency installation and all unit tests, then remained in the data-processing step for an extended period. This is recorded as a performance/observability issue; no research result is accepted until the run completes.
- The interactive tool session timed out while waiting for the long-running GitHub Actions job. This does not imply a backtest failure.

- Performance remediation: the first engine materialized a large global option dictionary and repeatedly scanned the full spot table for each expiry. It was replaced with expiry/strike predicate-pushed Parquet reads and per-expiry indices. The replacement also uses the historically applicable NIFTY lot size.

- 2026-10-01: Optimized engine failed on first Parquet query because the dataset timestamp is timezone-aware IST while filter bounds were timezone-naive. Fixed by constructing Asia/Kolkata-aware filter timestamps. No trade result was produced from the failed run.

- 2026-10-01: 2025 option processing completed through all 52 candidate expiries, but the run failed when the spot repository's 2026 directory used two date-range CSV filenames rather than `NIFTY50_1min_2026.csv`. Fixed by supporting both actual 2026 files and deduplicating their overlap.

- 2026-10-01: Data-quality output showed systematic missing entry legs for many early expiries. Root cause identified: candidate strikes for the filtered Parquet read were initially derived from the first 09:15 spot bar while the strategy enters at 10:00. The engine has been corrected to derive initial candidates from the actual 10:00 spot row; the next run is required to validate the correction.


## Phase 6 start — 2026-10-01
- V3 research restarted on a separate branch to prevent contamination of the completed V2 baseline.
- A new unit-tested cash-flow realization path is being used for V3 expiry liquidation.
- Any implementation or data issue found during V3 will be appended here before the phase is accepted.


## Phase 6 strategy reset — 2026-10-01
- The previous V2 profit-target/recentering strategy is frozen as a completed baseline and is not overwritten.
- V3 uses no profit target, exits at expiry, and applies one static OTM8 reversal as specified in research/strategy_spec_v3.md.
- V3 uses cash-flow-based expiry realization and explicit unit tests; this is isolated from the frozen V2 result files.


## Phase 6 workflow concurrency — 2026-10-01
- Four push-triggered V3 runs were started because documentation/status commits initially also matched the workflow push trigger.
- The latest run completed successfully; three older runs completed research steps successfully but failed only at the final git push because another run had already advanced the branch (fetch-first rejection).
- Workflow was corrected to trigger on research/code paths only and to use a concurrency group with cancel-in-progress, preventing documentation commits from launching redundant full backtests.

## Phase 6 research result
- V3 produced 84 validated trades (42 CE, 42 PE) from the available sample.
- No data-quality issue caused the accepted V3 result; missing historical option observations remain documented as skips.


## Phase 6 strategy reset — 2026-10-01
- The previous V2 profit-target/recentering strategy is frozen as a completed baseline and is not overwritten.
- V3 uses no profit target, exits at expiry, and applies one static OTM8 reversal as specified in research/strategy_spec_v3.md.
- V3 uses cash-flow-based expiry realization and explicit unit tests; this is isolated from the frozen V2 result files.
