# Research Plan — V5 Credit-Selected OTM6/7/8

## Research questions
1. Does the larger of the call and put credit measures at 10:00 select a structure with positive and repeatable net P&L?
2. What fraction of candidate expiries select calls versus puts?
3. How often does the 90%-of-flatline target trigger, and how often does the trade instead stop out or reach expiry?
4. What stop-loss multiple of the initial net credit provides the best validation performance without relying on the final holdout?
5. How sensitive are the conclusions to target fraction and execution slippage?
6. Are results stable across calendar periods, call/put selections and transaction-cost regimes?

## Aim
Evaluate the user-specified credit-selection rule and identify a data-supported stop-loss criterion using an untouched chronological holdout.

## Objectives
1. Reconstruct historical expiry dates from the option data rather than hard-code the current expiry weekday.
2. Enter exactly four trading sessions before each eligible expiry at 10:00 IST.
3. Build both OTM6/7/8 structures from the same entry spot and calculate both credits.
4. Select the larger positive credit.
5. Backtest a 90% flatline target with a pre-specified stop grid.
6. Select the stop only on the validation segment.
7. Freeze the selected stop and evaluate the final 20% chronology as untouched test data.
8. Include brokerage, statutory levies and adverse slippage.
9. Publish trade-level, selection, cost, target/stop and statistical outputs.

## Statistical analysis
- Descriptive: count, mean, median, total P&L, win rate, profit factor, worst/best trade, peak-to-trough drawdown, target-hit/stop-hit/expiry rates.
- Uncertainty: bootstrap 95% confidence interval for mean net P&L on the final test segment.
- Robustness: target fractions 85%, 90%, 95%, 100%; slippage 0, 0.10, 0.25 and 0.50 points.
- Stability: yearly/quarterly and call-vs-put selection breakdown.
- Leakage controls: all exits use a subsequent option-bar open after a close-based trigger.

## Chronological split
- Development: first 60% of eligible completed trades ordered by expiry date.
- Validation: next 20%; used only to select the stop-loss multiple.
- Test: final 20%; untouched until stop is frozen.

## Phase sequence
### Phase 9A — Specification and tests
Freeze structure, entry, side-selection, target and stop-search definitions.

### Phase 9B — Empirical backtest
Run the complete 2025–2026 available option sample with the pinned HF source and historical spot source.

### Phase 9C — Stop-loss selection
Select one stop multiple only from the validation segment, then lock it.

### Phase 9D — Untouched test and robustness
Evaluate the frozen stop on the final chronological test segment and run cost/target sensitivities without re-selecting the primary rule.

### Phase 9E — Manuscript and stopping rule
Record results, inferences, limitations and future work. No further parameter search in this phase.

<!-- Phase 9 execution trigger checkpoint: persistence-hardened workflow requires a fresh push-triggered run. -->
