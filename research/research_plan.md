# Final Stand V4 — Research Plan

## Current phase: Strategy V4 double-sided OTM16/17

This phase is a new branch and does not overwrite the frozen V2 or V3 result sets.

## Research question
What is the realized net P&L distribution and drawdown of the NIFTY 50 four-leg structure — buy 1 OTM16 CE, sell 2 OTM17 CE, buy 1 OTM16 PE, sell 2 OTM17 PE — entered 4 trading days before expiry at 10:00 IST and held to expiry, after modeled slippage and transaction costs?

## Aim
Evaluate the specified four-leg NIFTY structure with reproducible historical one-minute option data and explicit execution assumptions.

## Objectives
1. Reconstruct OTM16/OTM17 strikes from the 10:00 entry spot.
2. Use the fourth prior trading day, not a calendar-day shortcut, for entry.
3. Execute all four legs at the 10:00 option-bar open with modeled slippage.
4. Exit all legs at the established 15:29 expiry-bar-open convention.
5. Account for quantity-weighted turnover, brokerage, exchange charges, SEBI fee, stamp duty, STT and GST.
6. Produce trade-level, annual, monthly and aggregate statistics.
7. Record all data gaps as explicit skips.
8. Preserve V2/V3 results as immutable prior-phase baselines.

## Methodology
- Historical window: 2025–2026 available repository sample.
- Data sources: existing validated NIFTY 1-minute spot and option pipeline.
- Strike interval: 50 points for this sample.
- Entry spot proxy: 10:00 NIFTY bar open.
- Option execution proxy: 10:00 option bar open.
- Exit proxy: 15:29 option bar open on expiry.
- No profit target, trigger, roll or re-centering.
- Baseline costs: 0.10 option-premium points slippage per execution and INR 20 brokerage per executed order; both are workflow parameters.
- Lot size: 75 through 30-Dec-2025 expiry; 65 thereafter.

## Statistical analysis
Primary: trade-level count, mean/median net P&L, win rate, profit factor, total net P&L, worst/best trade, total costs and sequential trade-level drawdown.

Secondary: annual/monthly stability, gross-versus-net P&L decomposition, distribution shape, and sensitivity to cost parameters when explicitly run.

## Phase sequence
### Phase 7A — Specification and unit tests
Status: COMPLETE. Accepted CI run passed all 15 tests.

### Phase 7B — Full empirical backtest
Status: COMPLETE. GitHub Actions run 36929461356 passed the full 2025–2026 available sample.

### Phase 7C — Output validation
Status: COMPLETE.
43 unique complete trades were validated with 8 orders per trade, expiry-only exits, expected lot sizes, and explicit skips.

### Phase 7D — Statistical analysis
Status: COMPLETE.
Aggregate, yearly, monthly, cost, uncertainty and intratrade MTM metrics were generated.

### Phase 7E — Documentation and conclusion
Status: COMPLETE.
README, status, logs, results interpretation and manuscript were updated. This phase is closed.

## Stopping rule
No new strategy variants, parameter searches or regime mining are added unless a new phase/branch is created.
