# Strategy Specification V3 — Static OTM8 Reversal Hedge

## 1. Strategies

### Strategy 1 — Put
- Buy 1 × OTM6 Put
- Sell 1 × OTM7 Put
- Sell 1 × OTM8 Put

### Strategy 2 — Call
- Buy 1 × OTM6 Call
- Sell 1 × OTM7 Call
- Sell 1 × OTM8 Call

## 2. Entry
- Enter at exactly 4 DTE, 10:00 AM IST.
- OTM6/OTM7/OTM8 are selected from the entry spot using the 50-point NIFTY strike grid.

## 3. Exit
- No profit target.
- Hold until 0 DTE (expiry).
- For reproducible one-minute backtesting, expiry liquidation is executed at the 15:29 IST bar open.

## 4. Static OTM8 reversal rule
The trigger is based on the initial entry OTM8 strike and is not re-centered.

### Strategy 1 — Put
If NIFTY moves below the initial OTM8 PE strike before expiry:
1. Buy back the original short OTM8 PE.
2. At the next available minute, sell 1 × opposite-side option (CE) at the same strike as the initial OTM8 PE.
3. Keep the OTM6 PE and OTM7 PE unchanged.
4. Only one such reversal is permitted per trade.

### Strategy 2 — Call
If NIFTY moves above the initial OTM8 CE strike before expiry:
1. Buy back the original short OTM8 CE.
2. At the next available minute, sell 1 × opposite-side option (PE) at the same strike as the initial OTM8 CE.
3. Keep the OTM6 CE and OTM7 CE unchanged.
4. Only one such reversal is permitted per trade.

## 5. Trigger/execution convention
- Calls trigger when one-minute NIFTY high is strictly above initial OTM8.
- Puts trigger when one-minute NIFTY low is strictly below initial OTM8.
- Trigger observation at minute t is executed at minute t+1 open.
- A trigger in the final minute cannot be rolled and is liquidated at expiry.

## 6. Transaction costs
- ₹20 brokerage per executed option order.
- ₹0.10 premium-point slippage per execution.
- Date-aware NSE option transaction charges, SEBI fee, stamp duty, STT and GST.
- Historical bid/ask is unavailable, so slippage is modeled rather than reconstructed.

## 7. Accounting convention
- Buy entry decreases cash.
- Sell entry increases cash.
- Buyback of a short decreases cash.
- Sale of a long increases cash.
- Mark-to-market P&L = cash + signed market value of open positions.
- Expiry liquidation uses the same cash-flow convention.
- This accounting is unit-tested and isolated from the frozen V2 baseline.

## 8. Comparison
Compare Strategy 1 (PE) and Strategy 2 (CE) on trade count, total/mean/median net P&L, win rate, profit factor, worst trade, volatility, drawdown, roll frequency, costs, CE/PE descriptive ratios, and paired/non-parametric tests.

## 9. Non-goals
- No profit-target optimization.
- No re-centering after the reversal.
- No forward-looking or same-bar execution.

## Execution checkpoint
- The accepted V3 implementation permits at most one static OTM8 reversal per trade and does not re-center the trigger after the reversal.
