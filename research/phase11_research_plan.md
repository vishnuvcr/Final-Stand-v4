# Phase 11 Research Plan — NIFTY Spot-Based Stop-Loss Research

## Purpose
Evaluate whether an objective NIFTY spot-price barrier can provide a stop-loss rule for the frozen Phase 9 credit-selected OTM6/7/8 strategy, without using option premium/P&L as the trigger.

## Research questions
1. Do fixed NIFTY-point barriers reduce adverse path risk without materially degrading terminal net P&L?
2. Do percentage barriers behave differently from fixed-point barriers?
3. Does volatility-normalized distance (ATR) provide a more stable barrier across changing NIFTY levels/regimes?
4. Are effects different for PUT-selected and CALL-selected trades?
5. How often would spot stops trigger before the eventual target or expiry outcome?
6. What is the effect on maximum drawdown, MAE, capital-at-risk, win rate, profit factor and net P&L after all modeled costs?
7. Does a spot stop add information beyond the existing no-stop control?

## Frozen base strategy
- Entry: fourth prior trading session before nearest historical listed expiry, 10:00 IST.
- Structure: selected higher-positive-credit OTM6/7/8 1:-1:-1 PUT or CALL structure.
- Primary target: 90% of initial net-credit flatline.
- Control stop: Phase 9 validation-selected 0x/no-stop.
- Same strike mapping, lot sizes, execution, slippage and transaction-cost model.
- No re-centering, reversal, roll or missing-leg imputation.

## Candidate spot-stop families
All candidates are frozen before evaluation:
### A. Fixed points
50, 75, 100, 125, 150, 200 NIFTY points adverse from entry spot.
### B. Percentage
0.25%, 0.40%, 0.50%, 0.75%, 1.00% adverse from entry spot.
### C. ATR-normalized
0.50, 0.75, 1.00, 1.25, 1.50 × pre-entry ATR.
ATR must be computed only from information available before entry; no future bars may enter the ATR calculation.

## Trigger convention
For a PUT-selected structure, an adverse downward spot barrier is used; for a CALL-selected structure, an adverse upward spot barrier is used. This follows the piecewise expiry payoff of +1 PE(OTM6) - 1 PE(OTM7) - 1 PE(OTM8) and +1 CE(OTM6) - 1 CE(OTM7) - 1 CE(OTM8): below all put strikes the PUT structure has positive spot slope (downward is adverse), while above all call strikes the CALL structure has negative spot slope (upward is adverse). The direction is verified before backtest execution.

A completed 1-minute NIFTY spot bar whose high/low crosses the barrier triggers an exit at the first common executable next-minute option-bar open. Because OHLC data do not establish the intrabar ordering when target and spot stop are both signalled in the same completed minute, the pre-specified conservative convention is to give the spot stop precedence on that minute; no intrabar look-ahead is permitted.

## Statistical design
- Development: 60%, validation: 20%, untouched test: 20%, preserving Phase 9 chronological dates.
- Candidate parameters are selected only on validation.
- The untouched test is evaluated once after the candidate rule is frozen.
- Primary selection criterion: mean net P&L; tie-break median net P&L, then maximum drawdown.
- Secondary reporting: total P&L, win rate, profit factor, MAE/MFE, target-hit rate, stop-hit rate, expiry rate, premature-stop rate and capital-at-risk.
- Bootstrap confidence intervals will be reported for the final untouched-test mean where sample size permits.
- No exploratory context variable may be converted into a stop parameter.

## Execution-cost model
Retain Phase 9 assumptions:
- 0.10 premium points slippage per option execution.
- ₹10 brokerage per unique F&O order.
- Date-aware exchange/SEBI/STT/stamp/GST charges.
- Historical lot size rules.

## Data and provenance
- Reuse cached Phase 9 option data and NIFTY 1-minute data.
- Record source revisions/hashes and data-quality exclusions.
- No silent missing-data imputation.

## Deliverables
- research/phase11_research_plan.md
- research/phase11_sources.md
- research/phase11_status.md
- scripts/phase11_spot_stop.py
- tests/test_phase11_spot_stop.py
- .github/workflows/phase-11-nifty-spot-stop.yml
- results/phase11_candidate_grid.csv
- results/phase11_validation_selection.csv
- results/phase11_test_trades.csv
- results/phase11_final_summary.json
- results/phase11_data_quality.json
- error log and README updates

## Stopping rule
Run the predefined fixed-point, percentage and ATR grids once; select a rule only from chronological validation; evaluate it once on the untouched test; then freeze Phase 11. Any further stop family or additional parameter search requires Phase 12.
