# Strategy V5 — Credit-Selected OTM6/7/8 Single-Side Structure

## 1. Candidate structures
- Put structure: buy 1 × OTM6 PE; sell 1 × OTM7 PE; sell 1 × OTM8 PE.
- Call structure: buy 1 × OTM6 CE; sell 1 × OTM7 CE; sell 1 × OTM8 CE.

## 2. Entry
- Candidate expiry is the nearest listed NIFTY weekly/monthly expiry to the fourth prior trading session.
- Entry is 10:00 IST on exactly the fourth prior trading session.
- Initial ATM is the nearest 50-point strike to the 10:00 NIFTY spot.
- Tie at exactly 25 points is rounded upward.
- OTM6/7/8 are 6, 7 and 8 strike intervals from ATM.
- The six required entry option bars must be available at 10:00. No missing-leg imputation is allowed.

## 3. Side selection
At entry calculate:
- Put credit = PE(OTM7) + PE(OTM8) − PE(OTM6).
- Call credit = CE(OTM7) + CE(OTM8) − CE(OTM6).
- Select the side with the higher positive credit.
- If neither side has positive credit, the expiry is recorded as `no_positive_credit` and not traded. This preserves the meaning of a positive payoff-chart flatline.
- Exact ties are recorded and resolved deterministically in favour of the put structure.

## 4. Profit exit
- The payoff-chart flatline equals the initial net credit after entry slippage, multiplied by the historical contract lot size.
- Primary profit target = 90% of this flatline amount.
- The trigger is evaluated on completed one-minute closes after entry. The exit is executed at the first common executable option-bar open strictly after the trigger minute.
- If the target is not reached, the position remains open until 0 DTE.

## 5. Stop-loss search
- Candidate stop-loss levels are 0.50×, 0.75×, 1.00×, 1.25× and 1.50× the initial net credit, plus a no-stop baseline.
- Stop-loss trigger = running net MTM <= −stop_multiple × initial net credit × lot size.
- Trigger evaluation uses one-minute closes; execution is at the first common executable option-bar open strictly after the trigger minute.
- The stop multiple is selected using only the chronological validation segment, with validation mean net P&L as the primary criterion and median net P&L then maximum drawdown as tie-breakers.
- The selected stop is frozen before the untouched final test segment is evaluated.

## 6. Expiry exit
- If neither target nor stop triggers, close at 15:29 IST expiry-day option-bar open.

## 7. Execution costs
- Baseline entry/exit slippage: 0.10 option-premium points per leg, adverse to the transaction.
- Paytm Money brokerage: ₹10 per executed unique order.
- NSE transaction charge: ₹3,503 per crore of option premium turnover until 29-Feb-2026 and ₹3,553 per crore from 1-Mar-2026.
- SEBI turnover fee: ₹10 per crore of turnover.
- Equity-option stamp duty: 0.003% on buy-side premium turnover.
- STT: 0.10% on option-sale premium turnover through 31-Mar-2026; 0.15% from 1-Apr-2026.
- GST: 18% on brokerage + exchange transaction charge + SEBI fee.
- Historical NIFTY lot size: 75 through 30-Dec-2025 expiry; 65 thereafter.

## 8. Data scope
- Primary intraday options: pinned Hugging Face `rissin/nse-options-intraday`, 1-minute NIFTY options.
- Underlying entry/holding spot: pinned public NIFTY 1-minute source already used by the repository's Phase 7 pipeline.
- Sample window: 2025-01-01 through 2026-09-30.

## 9. No hidden adaptive rules
- No dynamic OTM8 re-centering.
- No reversal/roll.
- No look-ahead using the same minute close for an execution price.
- No filling of missing option observations.