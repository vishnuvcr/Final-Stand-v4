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


## Phase 7 CI test error — 2026-10-02
- GitHub Actions run 36928921436 failed in the V4 unit-test stage before the backtest because the expected PE strike values in test_v4_strategy.py were incorrect for entry spot 24,486.3.
- Actual V4 mapping is ATM 24,500; PE16 = 23,700 and PE17 = 23,650. The erroneous test expected 23,650 and 23,600.
- No performance output was produced by this failed run. The test expectation is corrected before rerun.


## Phase 7 data-loader error — 2026-10-02
- GitHub Actions run 36929127871 passed all 15 unit tests and completed all 52 candidate expiries for 2025.
- The backtest then failed at 2026 spot loading because the source repository no longer contains the previously used range filenames. The current public directory uses monthly files named NIFTY50_1min_2026-01.csv through NIFTY50_1min_2026-10.csv.
- No V4 performance output is accepted from this run. The spot loader is being updated to the currently observed repository layout.


## Phase 7 accepted rerun — 2026-10-02
- GitHub Actions run 36929461356 passed all 15 tests, completed the full 2025–2026 available sample, ran analysis, and committed outputs.
- Final accepted results: 43 complete trades, 49 documented skips, total net P&L INR 84,698.69.
- Validation confirmed 43 unique expiry trades, 8 orders per complete trade, expiry-only exits, and expected lot sizes.
- The remaining data-quality limitation is historical source incompleteness, not an unresolved engine error.


## Phase 8 source-audit tooling error — 2026-10-02
- First attempt to create `research/phase8_data_source_audit.md` failed before any commit because the generated tool payload contained unescaped backtick delimiters inside a JavaScript template literal.
- No repository state was changed by the failed attempt. The file was then created using a newline-array payload and committed successfully.


## Phase 8B recovery execution — 2026-10-02
- Added targeted recovery against the independent public TradeMarkk/Hugging Face NIFTY expiry-file dataset.
- Recovery outputs are intentionally separate from Phase 7 and will not be merged until contract/timestamp validation passes.

## Phase 8B acquisition/access limitation — 2026-10-02
- The connected GitHub interface does not expose workflow dispatch/readback sufficiently to verify the newly created recovery workflow result.
- No recovered trades were accepted from an unverified workflow.
- Public web research identified a complete commercial NIFTY 1-minute full-chain archive through Sep-2026 and official ICICI Breeze contract-level historical API documentation, but no authorized credentials/archive are available in the current session.
- Preventive rule: never manufacture a recovery result or silently replace Phase 7 observations.


## Phase 9 initialization — 2026-10-02
- The first GitHub file-write attempt for the stop-analysis script passed a JavaScript array instead of a string to the repository file API. The write was rejected before repository modification. No scientific output was affected.
- The initial Phase 9 candidate-expiry implementation risked treating every expiry-date row in the options dataset as a near-weekly candidate, which could have introduced far-dated duplicates. Before any run, this was corrected to require (a) the expiry to be the nearest listed expiry on the entry date and (b) entry-to-expiry distance no greater than eight calendar days.
- Preventive rule: never assume the current Tuesday NIFTY expiry convention for earlier 2025 contracts; historical contract expiry dates must come from the dataset or a date-effective exchange source.
- Preventive rule: the primary target/stop grid is frozen before reading performance outputs; no post-hoc stop selection from the final holdout.


## Phase 9 data-source correction — 2026-10-02
- GitHub Actions run 36966020688 failed because the pinned Hugging Face revision 78b1c54 did not contain upstox_intraday/NIFTY/NIFTY_2026.parquet. No strategy results were accepted.
- The engine was corrected to resolve the current dataset commit SHA from HF at runtime, then download both annual files at that same resolved revision. The resolved SHA is recorded in the output provenance.
- During the same audit, exit transaction charges were found to be using the entry date. The engine was corrected so exit fees use the actual exit timestamp/date, which matters for the March/April 2026 fee-rate changes.
- Preventive rule: a source revision is not accepted merely because a prior README mentioned it; the exact requested file paths must be validated at runtime.