# Strategy Specification V4 — Double-Sided OTM16/17 Structure

## Strategy
NIFTY 50 index options:
- Buy 1 OTM16 Call
- Sell 2 OTM17 Call
- Buy 1 OTM16 Put
- Sell 2 OTM17 Put

OTM levels are measured from the NIFTY entry spot using the 50-point strike grid:
- OTM16 CE = ATM + 16 x 50
- OTM17 CE = ATM + 17 x 50
- OTM16 PE = ATM - 16 x 50
- OTM17 PE = ATM - 17 x 50

## Entry
- Enter exactly 4 trading days before expiry.
- Entry time: 10:00 IST.
- The 10:00 IST NIFTY 1-minute open is used as the entry spot proxy so strike selection does not use the 10:00 close.
- All option entries use the 10:00 IST option-bar open with configured slippage.

## Exit
- No intermediate profit target, roll, reversal, or re-centering rule.
- Hold through expiry (0 DTE).
- Expiry liquidation convention: 15:29 IST option-bar open, matching the project's established one-minute expiry convention.

## Execution and accounting
- Long quantity: 1 contract.
- Short quantity: 2 contracts.
- Brokerage is configurable; baseline is INR 20 per executed order for continuity with the prior phase.
- Premium slippage is configurable; baseline is 0.10 premium points per execution.
- Date-aware NSE option transaction charges, SEBI fee, stamp duty, STT and GST use the project's existing parameterization.
- Historical bid/ask is unavailable in the selected public intraday dataset, so slippage is modeled rather than reconstructed.
- Gross P&L is before modeled fees; net P&L is after modeled costs.

## Historical sample
- Primary bounded run: 2025-2026 using the validated repository data pipeline.
- Missing observations produce documented skips, not imputed trades.
- Historical NIFTY lot size: 75 through the 30-Dec-2025 expiry and 65 thereafter, matching the existing project record.
