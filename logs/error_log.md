# Error Log

## 2026-10-01
- No research-code error yet.
- Repository was initially empty; baseline research files were initialized during strategy-specification setup.
- A previous interpretation used a fixed OTM8 to OTM12 to OTM16 roll. This is superseded by V2: re-calculate OTM8 from the current spot after each trigger.

## Phase 1 infrastructure errors — 2026-10-01
- GitHub Actions runs initially failed because the cache key contained a comma from the YEARS input. Fixed by removing YEARS from the cache key.
- The current Phase 1 backtest run passed dependency installation and all unit tests, then remained in the data-processing step for an extended period. This is recorded as a performance/observability issue; no research result is accepted until the run completes.
- The interactive tool session timed out while waiting for the long-running GitHub Actions job. This does not imply a backtest failure.
- Performance remediation: the first engine materialized a large global option dictionary and repeatedly scanned the full spot table for each expiry. It was replaced with expiry/strike predicate-pushed Parquet reads and per-expiry indices. The replacement also uses the historically applicable NIFTY lot size.
- 2026-10-01: Optimized engine failed on first Parquet query because the dataset timestamp is timezone-aware IST while filter bounds were timezone-naive. Fixed by constructing Asia/Kolkata-aware filter timestamps. No trade result was produced from the failed run.
- 2026-10-01: 2025 option processing completed through all 52 candidate expiries, but the run failed when the spot repository's 2026 directory used two date-range CSV filenames rather than NIFTY50_1min_2026.csv. Fixed by supporting both actual 2026 files and deduplicating their overlap.
- 2026-10-01: Data-quality output showed systematic missing entry legs for many early expiries. Root cause: candidate strikes for the filtered Parquet read were initially derived from the first 09:15 spot bar while the strategy enters at 10:00. The engine was corrected to derive initial candidates from the actual entry spot.

## Phase 6 strategy reset — 2026-10-01
- V3 was isolated on a separate branch to prevent contamination of the completed V2 baseline.
- V3 uses no profit target, exits at expiry, and applies one static OTM8 reversal.
- V3 uses cash-flow-based expiry realization and explicit unit tests.

## Phase 7 V4 initialization — 2026-10-02
- First attempt to generate the V4 repository files failed before any commit because the tool payload contained unescaped template-literal delimiters from GitHub Actions syntax and markdown backticks. No repository state was changed by that failed attempt.
- Corrected approach: write each V4 file with escaped workflow expressions and without embedded template delimiters.
- V4 also deliberately uses 4 trading days before expiry rather than the older calendar-day shortcut.
- V4 uses the 10:00 spot open rather than the same-minute spot close for strike selection to avoid within-minute look-ahead.

## Preventive rule for V4
- Do not accept performance outputs until unit tests, data-quality checks and the final ledger are all present.
- Documentation-only commits are excluded from the V4 workflow push-path trigger to avoid redundant long backtests.
