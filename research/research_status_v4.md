# Research Status — Phase 7 / Strategy V4

## Current status
**PHASE 8A COMPLETE — SOURCE DISCOVERY; ACQUISITION PENDING**

## Frozen specification
- Buy 1 OTM16 CE.
- Sell 2 OTM17 CE.
- Buy 1 OTM16 PE.
- Sell 2 OTM17 PE.
- Entry: 4 trading days before expiry, 10:00 IST.
- 10:00 spot open determines the 50-point strike ladder.
- Option execution uses the 10:00 option-bar open with modeled slippage.
- Exit: 0 DTE / expiry at 15:29 option-bar open.
- No target, rolling, re-centering or reversal.
- Baseline slippage: INR 0.10 premium points per execution.
- Baseline brokerage: INR 20 per executed order.
- Existing date-aware exchange, SEBI, STT, stamp-duty and GST model retained.
- Missing data is skipped and documented.

## Phase execution history
### Phase 7A — Specification and tests
**COMPLETE**
- Final strategy specification committed.
- 15 repository tests passed in the accepted run.

### Phase 7B — Full empirical backtest
**COMPLETE**
- GitHub Actions run 36929461356 passed.
- 2025–2026 candidate expiries processed.
- 43 complete four-leg trades accepted.
- 49 candidates skipped.

### Phase 7C — Validation
**COMPLETE**
- 43 unique expiry trades.
- 8 orders per complete trade.
- All exits are expiry exits at the specified 15:29 convention.
- Historical lot sizes present are 75 and 65 as expected.
- No terminal net-loss trade in the accepted sample.
- All 43 accepted trades experienced negative intratrade gross MTM.

### Phase 7D — Statistical/descriptive analysis
**COMPLETE**
- Total net P&L: INR 84,698.69.
- Mean net P&L/trade: INR 1,969.74.
- Median net P&L/trade: INR 733.62.
- Terminal win rate: 43/43 = 100%.
- Modeled costs: INR 8,551.66, 9.17% of gross P&L.
- Worst intratrade gross MTM: -INR 24,394.50.
- Maximum peak-to-trough gross MTM swing: INR 29,113.50.

### Phase 7E — Documentation and conclusion
**COMPLETE**
- Results interpretation documented.
- Research manuscript created.
- Risk-analysis output created.
- README, plan, decision log and error log updated.
- V2/V3 historical baselines preserved.

## Main conclusion
The accepted complete-trade sample was profitable at expiry after modeled costs, but the strategy experienced substantial interim MTM losses and the source-data coverage was incomplete. Terminal win rate therefore must not be interpreted as low path risk.

## Research stopping rule
This phase is closed. New exit rules, strike distances, capital models, regime filters, or parameter searches require a new branch/phase.


## Phase 8 — Option Data Source Recovery
### Phase 8A — Source discovery
**COMPLETE**
- Reviewed official ICICI Breeze documentation for 1-minute NFO option history.
- Reviewed TradeMarkk/Hugging Face 1-minute index-options data.
- Reviewed commercial full-chain options data and Global Datafeeds.
- Reviewed Zerodha-derived collectors and Dhan historical-data limitations.
- No Phase 7 result has been altered.

### Phase 8B — Targeted source acquisition
**NOT STARTED**
- Objective: recover the 49 skipped candidate expiries where the required 10:00 and/or 15:29 option observations are genuinely available from an independent source.
- Acceptance requires contract/timestamp validation and source provenance.
