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
- First attempt to create research/phase8_data_source_audit.md failed before any commit because the generated tool payload contained unescaped backtick delimiters inside a JavaScript template literal.
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

## Phase 9 result-persistence error — 2026-10-02
- Run 36966258307 completed the full Phase 9 computation and generated 11 result files in the runner workspace.
- The workflow's final git push failed with a non-fast-forward rejection because the remote phase branch had advanced after checkout.
- The generated numerical outputs were therefore not persisted to the repository. No numbers from this run should be treated as reproducibly archived until the persistence rerun succeeds.
- Workflow correction committed: the Phase 9 commit step now fetches and rebases against origin/phase-9-credit-selected-otm6-8 before pushing.

## Phase 9 resolution — 2026-10-02
- Hardened workflow run 36970175719 completed successfully.
- Unit tests passed; the full computation completed with 56 executable trades and 26 skipped candidates.
- The workflow created output commit d03d7a1 and successfully pushed it to phase-9-credit-selected-otm6-8 after fetch/rebase.
- All 11 expected Phase 9 result files are now present on the remote branch and were re-read successfully, closing the persistence error.
- Preventive rule retained: numerical outputs are not accepted until both the workflow persistence step and remote file readback succeed.


## Phase 10 initialization — 2026-10-02
- Phase 10 was opened on separate branch phase-10-v5-robustness-context so Phase 9 remains frozen.
- Plan, source register, status file, robustness runner, tests and manual workflow were committed.
- Initial GitHub Actions discovery for the new branch returned no workflow run. The connected GitHub interface does not expose workflow-dispatch POST, so no unverified computation is being claimed.
- Preventive rule: do not mark Phase 10 computational outputs complete until a workflow run passes tests, executes the runner, persists outputs and remote readback succeeds.

## Phase 10 closure correction — 2026-10-02
- The first Phase 10 computation completed successfully, but post-run audit found that the runner had implemented separate slippage and brokerage sensitivities rather than the full pre-specified 4×3 Cartesian cost grid.
- This was a methodology-completeness error, not a numerical backtest failure. The runner was corrected to execute all 12 slippage×brokerage combinations and to persist \`results/phase10_cost_stress.csv\`.
- The same audit found that market-context acquisition had not yet been executed. A provenance-preserving acquisition step was added for official NSE NIFTY 50/India VIX/FII-DII sources plus independent daily global/USDINR/gold validation sources.
- No Phase 10 closure claim is accepted until the corrected workflow persists and remote-readback verifies the full outputs.


### Phase 10 closure correction — 2026-10-02 (continued)
- Added `scripts/phase10_context_join.py` and workflow execution step so the planned `results/phase10_market_context.csv` is actually produced when validated source files are available.
- Context joins are lagged to the prior available daily observation; missing variables are left missing and reported through coverage flags.
- No corporate/news regime filter is inferred when reproducible historical coverage is unavailable.


### Tooling error — 2026-10-02
- Attempted to inspect the Phase 10 branch with the GitHub `fetch` tool using repository/ref arguments.
- The tool contract requires a public GitHub URL, so the call was rejected before any repository modification.
- No research data or methodology was affected. Future branch inspection will use the repository-specific file/run tools or an approved GitHub URL.


### Tooling limitation — 2026-10-02
- Attempted to query the repository Actions workflow-run collection through the generic GitHub URL fetcher.
- The connector rejected the Actions API URL as outside its allowed public-repository endpoint set.
- No repository modification occurred. Workflow execution therefore remains unverified through the available tooling.


### Infrastructure limitation — 2026-10-02
- Attempted a direct local clone of the Phase 10 branch to execute the corrected workflow outside GitHub Actions.
- The execution environment could not resolve `github.com`, so the clone failed before data or repository contents were downloaded.
- No calculations were accepted from this attempt. GitHub Actions remains the authoritative execution path for the cached-data research workflow.


### Execution-status correction — 2026-10-02
- Earlier connector checks incorrectly suggested that the push-triggered workflow might not have fired because the available workflow-run connector filters commit-associated results to pull-request-triggered runs.
- User-provided GitHub Actions evidence confirms the Phase 10 workflow is in fact running/queued: an earlier closure run is **In progress** and the newest corrected closure trigger is **Pending**.
- No scientific result was affected; this only corrects the execution-status interpretation.


### Phase 10 execution-concurrency correction — 2026-10-02
- The corrected closure workflow runs were repeatedly queued behind a stale long-running run (run 36975859064), while subsequent push-triggered runs were cancelled by the repository's `cancel-in-progress: false` concurrency setting.
- This is an infrastructure/execution-control issue, not a research-methodology change. The Phase 10 workflow was changed to `cancel-in-progress: true` so the newest corrected closure run supersedes stale execution and can complete the predefined analysis.
- No numerical result from the cancelled runs is accepted. Acceptance remains gated on tests, completion, persistence and remote readback.


### Phase 10 test syntax error — 2026-10-02
- Corrected closure run 36979199194 failed during pytest collection because `tests/test_phase10_context.py` contained an unescaped nested quote in the assertion for `direction="backward"`.
- No Phase 10 numerical computation ran from this failed execution, so no result is accepted from it.
- The test assertion will be corrected and the workflow rerun. Scientific methodology is unchanged.


### Phase 10 robustness-run efficiency correction — 2026-10-02
- Audit of the corrected closure runner found redundant full backtest executions: brokerage changes cannot affect target triggering because brokerage is charged after execution and the strategy has no stop.
- The runner was therefore refactored to execute the four target cases and four distinct slippage cases, then derive the three brokerage levels exactly from each slippage ledger using the brokerage-plus-GST difference multiplied by the recorded order count.
- This preserves the predefined 4×3 Cartesian economic scenarios while materially reducing repeated data processing. It is an execution optimization, not a strategy or parameter change.


### Phase 10 context-join JSON parsing error — 2026-10-02
- Corrected robustness execution 36980075489 completed the full computational robustness grid and market-context acquisition successfully, but context joining failed because the NSE NIFTY history response saved by the acquisition step was not valid JSON (NSE returned a non-JSON response in the automated environment).
- The join script previously treated that response as mandatory and raised JSONDecodeError.
- The join was corrected to treat unavailable/malformed NSE context as missing rather than crashing, and to use the independently acquired Stooq NIFTY series as a validated secondary fallback for NIFTY close/realized-volatility context.
- India VIX and FII/DII remain coverage-gated; unavailable series will be reported missing rather than fabricated.


## Phase 10 context-source validation correction — 2026-10-02
- The successful closure workflow persisted the context-join file, but remote readback showed it contained only the strategy ledger: the NSE JSON responses and Stooq CSV responses were syntactically acquired but did not parse into usable context series.
- This is a data-acquisition/validation gap, not a change to the trading rule or backtest ledger. The gap is explicitly logged rather than treating an empty context join as evidence of no relationship.
- Added a validated NSE/Nifty-Indices client fallback for NIFTY 50 and India VIX plus a public historical FII/DII JSON fallback. Normalized files are cached under `data_cache/phase10_context_raw` during the workflow and joined with the existing prior-observation, no-look-ahead rule.
- Scientific parameters remain frozen; context remains descriptive only.
