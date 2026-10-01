# Research Status — Phase 7 / Strategy V4

## Current status
**BACKTEST EXECUTING IN GITHUB ACTIONS**

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

## Phase sequence
1. Specification and unit tests — ACTIVE/COMPLETE once CI test stage passes.
2. Full 2025-2026 backtest — RUNNING.
3. Output validation and error correction — PENDING.
4. Descriptive/statistical analysis — PENDING.
5. README/log update and phase conclusion — PENDING.

## Research stopping rule
Stop this phase after the backtest, validation, descriptive statistics, and documented limitations are complete. Any parameter expansion or different exit rule requires a new strategy phase.


## Backtest run 3 — 2026-10-02
- Status: **REJECTED FOR ANALYSIS**
- Unit tests: **15 passed**.
- 2025 processing: **52/52 candidate expiries processed**.
- 2026 processing failed before the first expiry because the spot-source filename layout changed.
- Corrective action: update the 2026 spot loader to monthly source files and rerun the full 2025–2026 sample.


## Backtest execution
- Status: EXECUTED
- Trades: 43
- Skips: 49
