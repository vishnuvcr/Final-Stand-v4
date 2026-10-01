# Strategy Specification V2 — Dynamic OTM8 Re-centering

## 1. Initial structures
### Strategy 1 — Put
- Buy 1 × OTM6 PE
- Sell 1 × OTM7 PE
- Sell 1 × OTM8 PE

### Strategy 2 — Call
- Buy 1 × OTM6 CE
- Sell 1 × OTM7 CE
- Sell 1 × OTM8 CE

## 2. Entry
- Enter at exactly 4 DTE, 10:00 AM India time, using the actual NIFTY expiry calendar.
- OTM levels are defined from the entry spot and the available NIFTY strike grid.

## 3. Profit exit
- Calculate the initial expiry payoff and identify its approximately flat profit level.
- Exit all legs when realized/unrealized running P&L reaches the predefined target close to that initial flatline amount.
- If the target is not reached, exit at 0 DTE under the final execution convention selected for the backtest.

## 4. Dynamic OTM8 rule — revised
- Store the initial OTM8 strike at entry.
- If NIFTY crosses beyond that OTM8 before expiry, close/buy back that short OTM8 option.
- Determine a NEW OTM8 from the CURRENT NIFTY spot and the same strike-grid convention.
- Sell that newly calculated OTM8 option.
- If NIFTY subsequently crosses beyond this new OTM8, repeat the process.
- Thus the short far leg is re-centered to current spot each time its current OTM8 boundary is breached. It is NOT rolled by a fixed number of strike intervals.

## 5. Example from the supplied screenshot
Screenshot spot = 23,205.20; strike interval = 50.

Initial put ladder:
- OTM6 PE = 22,900
- OTM7 PE = 22,850
- OTM8 PE = 22,800

Initial call ladder:
- OTM6 CE = 23,500
- OTM7 CE = 23,550
- OTM8 CE = 23,600

For the put strategy, if NIFTY falls through 22,800, the 22,800 PE short is bought back. A fresh OTM8 PE is then calculated from the CURRENT spot and sold. For example, if the current spot were 22,740 and the strike grid remained 50 points, the nearest ATM strike would be 22,750 and OTM8 PE would be 22,350. The next trigger becomes 22,350. This example is illustrative; the backtest must use the exact exchange strike-selection rule.

For the call strategy, if NIFTY rises through 23,600, the 23,600 CE short is bought back. A fresh OTM8 CE is calculated from CURRENT spot and sold. For example, if current spot were 23,660, the nearest ATM strike would be 23,650 and OTM8 CE would be 24,050. The next trigger becomes 24,050.

## 6. Important interpretation
The phrase “another 8 far beyond” is interpreted as “another OTM8 calculated from the current spot,” not “eight strike intervals beyond the previous OTM8.” If this is not intended, the implementation must be changed before the backtest.

## 7. Execution assumptions to be explicitly tested
- Bid/ask-aware execution rather than idealized mid-price only.
- Slippage.
- Brokerage and statutory transaction costs, including the user's stated Paytm Money context where applicable.
- Actual option contract/lot-size changes through the historical sample.
- Exact expiry and holiday/calendar handling.
- Intraday trigger detection and ordering when multiple events occur in the same bar.
