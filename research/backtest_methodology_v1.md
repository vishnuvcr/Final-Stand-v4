# Backtest Methodology V1

## Scope
Primary empirical window: October 2024 onward, subject to validated intraday data availability. Initial CI run is configured for 2025–2026 to keep the first run bounded; the workflow can expand the years after validation.

## Data
- NIFTY 1-minute option OHLC from the public Hugging Face dataset rissin/nse-options-intraday, sourced from Upstox historical API and documented as Oct 2024→2026.
- NIFTY 1-minute spot OHLC from the public GitHub technovusin/nifty50-historical-data repository.
- NSE contract specifications and historical derivatives archives are exchange-reference validation sources.

## Entry
For each eligible NIFTY expiry, entry date is expiry minus exactly 4 calendar days. A trade is created only if that date is a trading day. Entry timestamp is 10:00 IST. Initial ATM is the nearest 50-point strike; OTM n is ATM ± n×50 for calls/puts under the current 50-point weekly/monthly strike regime. Historical regimes must be checked before extending the sample earlier than the current regime.

## Initial legs
- Put: +1 OTM6 PE, -1 OTM7 PE, -1 OTM8 PE.
- Call: +1 OTM6 CE, -1 OTM7 CE, -1 OTM8 CE.

## Profit target
The expiry payoff flatline for the initial structure equals the initial net premium credit when all three legs expire OTM. Base target = 100% of this initial gross flatline; sensitivity runs should test 90%, 95%, and 100%.

## Dynamic OTM8
When spot crosses the current OTM8 boundary before expiry: buy back the current short OTM8; recalculate OTM8 using the observed spot at the trigger minute; sell the newly calculated OTM8; repeat after every subsequent crossing.

The first implementation evaluates the trigger on 1-minute spot closes and executes the roll on the next available minute open to avoid look-ahead. This is a research approximation and should be sensitivity-tested against intrabar high/low trigger variants.

## Pricing / slippage
Entry and roll execution use the executable bar open with configurable fixed premium slippage. The public dataset does not provide historical bid/ask, so exact market-depth execution cannot be reconstructed. Slippage sensitivity is therefore mandatory.

## Costs
Brokerage is configurable per executed order because Paytm Money public pages contain differing historical/tier references; the current F&O FAQ states ₹10 per executed order, while other Paytm Money material references ₹20 for newer users. Both values should be tested. Statutory charges are parameterized and must be reconciled to exact historical rates before final manuscript publication.

## Expiry
If the target is not hit, positions are closed at the final available intraday bar on expiry. A separate settlement/intrinsic-value variant should be run as robustness analysis.

## Outputs
Trade-level ledger, call/put summary, target-hit rate, net P&L, win rate, drawdown, average/median trade, roll count, holding time, cost sensitivity, slippage sensitivity, and data-quality diagnostics.

## Contract-lot treatment
The lot size is time-varying rather than fixed. NSE revised NIFTY 50's market lot from 75 to 65 effective after the 30-Dec-2025 expiry; therefore 2025 expiries through 30-Dec use 75 and 2026 expiries use 65 in the initial implementation. This is validated against the NSE circular before final analysis.

## Current exchange references
NSE currently specifies Tuesday expiry for NIFTY 50 index options, with the previous trading day used when Tuesday is a trading holiday; current weekly/monthly NIFTY strikes use a 50-point interval. These rules are not retroactively assumed for earlier regimes.

## Execution convention correction
A profit target detected on a minute close is executed at the next available minute open, avoiding look-ahead. Roll detection similarly uses the trigger minute close and executes the buyback/new sale on the next minute open.
