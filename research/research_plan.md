# Final Stand V4 — Research Plan

## Research question
Does the NIFTY 50 three-leg 1:-1:-1 structure (long OTM6, short OTM7, short OTM8) entered at 4 DTE and 10:00 IST, with profit exit near the initial payoff flatline and dynamic current-spot OTM8 re-centering after each OTM8 breach, exhibit a repeatable risk-adjusted performance difference between call and put variants after realistic costs and slippage?

## Secondary questions
1. How often is the flatline target reached before expiry?
2. How frequently does dynamic OTM8 re-centering occur, and how does it affect P&L and drawdown?
3. Are call and put outcomes different across market regimes?
4. How sensitive are results to target fraction, slippage and brokerage assumptions?
5. How much of the apparent edge survives after execution costs?

## Aim
Quantitatively evaluate the specified call and put strategies using reproducible historical NIFTY option data, with explicit execution and data-quality assumptions.

## Objectives
- Build a validated expiry/trading-date calendar.
- Reconstruct OTM6/7/8 from entry spot using the applicable historical strike scheme.
- Implement current-spot OTM8 re-centering without look-ahead.
- Model entry, rolls and exits with configurable slippage and transaction costs.
- Produce trade-level and aggregate statistics.
- Compare call and put distributions without ranking them as a recommendation.
- Test robustness across target fractions, slippage, brokerage and expiry-exit conventions.
- Document data gaps, failed tests and implementation changes.

## Phases
### Phase 0 — Specification and literature/data review
Status: COMPLETED.

### Phase 1 — Data acquisition and validation
Status: IN PROGRESS.
- Acquire/cache NIFTY intraday options and spot.
- Validate schema, timestamps, expiries, strike availability and missingness.
- Reconcile samples with NSE EOD records.

### Phase 2 — Backtest engine validation
- Unit tests for strike mapping, trigger logic, no-look-ahead ordering, P&L accounting and expiry settlement.
- Synthetic path tests covering no breach, one breach and multiple re-centering events.

### Phase 3 — Full empirical backtest
- Full available intraday sample.
- Call and put variants.
- 90/95/100% target sensitivity.
- Brokerage 10/20 INR per order.
- Multiple slippage assumptions.

### Phase 4 — Statistical analysis and robustness
- Descriptive statistics.
- Bootstrap confidence intervals for mean/median trade P&L and win rate.
- Difference-in-distributions tests between call and put samples.
- Regime-stratified analysis using realized NIFTY volatility and direction.
- Multiple-testing controls where parameter grids are expanded.

### Phase 5 — Research manuscript
- Abstract, introduction, methods, results, discussion, limitations, conclusion, future work.
- Tables, charts, appendices, data dictionary and reproducibility instructions.

## Statistical analysis
Primary: trade-level net P&L distribution, median/mean, win rate, profit factor, maximum drawdown, target-hit rate and bootstrap 95% confidence intervals.

Secondary: Mann–Whitney U for distributional differences, permutation tests for mean/median differences, effect sizes, and regime-stratified comparisons. Because trades overlap in calendar time across call/put variants, paired analyses will be considered where trade dates align; otherwise independence assumptions will not be imposed without justification.

## Interpretation rule
The research will report measured differences and uncertainty. It will not convert the comparison into a trading recommendation or claim predictive certainty.

## Stopping rule
Research stops after Phase 5 and the predefined robustness grid. New exploratory branches require an explicit change to this plan and a new phase/branch.
