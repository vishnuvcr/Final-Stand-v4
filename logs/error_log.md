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
