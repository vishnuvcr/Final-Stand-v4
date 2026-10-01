# Phase 7 V4 — Results, Interpretation and Validation

## Research question
What is the realized net P&L distribution, path risk and data-quality profile of the NIFTY four-leg structure:
- Buy 1 OTM16 Call
- Sell 2 OTM17 Call
- Buy 1 OTM16 Put
- Sell 2 OTM17 Put
entered 4 trading days before expiry at 10:00 IST and held to expiry?

## Accepted methodology
- Historical sample: 2025–2026 available repository sample.
- Entry: fourth previous trading day before each expiry, 10:00 IST.
- Strike reference: 10:00 NIFTY spot bar open; 50-point strike grid.
- Execution: 10:00 option-bar open with ₹0.10 premium-point slippage per execution.
- Exit: expiry-day 15:29 option-bar open.
- Orders: four entry orders + four exit orders = 8 orders per complete trade.
- Costs: ₹20 brokerage per order plus the repository's modeled exchange charges, SEBI fee, stamp duty, STT and GST.
- Lot size: 75 through 30-Dec-2025 expiry and 65 thereafter.
- Missing source observations are skipped, never imputed.

## Data-quality result
There were 92 candidate expiries in the 2025–2026 spot sample and 43 complete four-leg trades, giving 46.74% usable coverage.

49 candidates were skipped:
- 47 for missing at least one required entry option leg.
- 1 for no 10:00 spot observation.
- 1 for insufficient prior trading days.

The skip pattern is material: 2025 yielded 15 accepted trades out of 52 candidates, while 2026 yielded 28 out of 40. The results therefore describe the **available complete-trade sample**, not an unbroken 2025–2026 weekly population.

## Terminal P&L results
| Metric | Result |
|---|---:|
| Complete trades | 43 |
| Terminal net win rate | 100.00% (43/43) |
| Total gross P&L | ₹93,250.35 |
| Total modeled costs | ₹8,551.66 |
| Total net P&L | ₹84,698.69 |
| Mean net P&L/trade | ₹1,969.74 |
| Median net P&L/trade | ₹733.62 |
| Std. dev. net P&L/trade | ₹3,468.47 |
| Worst terminal net trade | ₹38.27 |
| Best terminal net trade | ₹16,743.46 |
| Profit factor | Infinite/undefined because there were no terminal net losses |

Modeled costs consumed 9.17% of gross P&L. Average modeled cost was ₹198.88 per complete trade.

A 95% Student-t confidence interval for the mean net P&L per accepted trade is approximately **₹902 to ₹3,037**, treating trade observations as independent for this descriptive calculation. That independence assumption is not guaranteed for weekly overlapping market regimes and should not be read as a predictive interval.

For the observed 43/43 terminal win rate, the two-sided 95% Clopper–Pearson lower bound is approximately **91.78%**. This is a sample uncertainty calculation, not evidence that future trades will have the same win rate.

## Yearly results
### 2025
- 15 accepted trades
- Net P&L: ₹5,580.28
- Mean net/trade: ₹372.02
- Median net/trade: ₹270.34
- Terminal win rate: 100%

### 2026
- 28 accepted trades
- Net P&L: ₹79,118.41
- Mean net/trade: ₹2,825.66
- Median net/trade: ₹1,261.77
- Terminal win rate: 100%

The aggregate result is therefore dominated by a smaller set of high-volatility 2026 trades, especially March–April 2026.

## Path-risk result
The 100% expiry win rate is **not** equivalent to low risk.

All 43 accepted trades experienced a negative one-minute gross MTM observation before expiry. The worst observed gross MTM trough was **-₹24,394.50** on the trade entered 18-Mar-2026 for expiry 24-Mar-2026. That trade ultimately closed with **+₹3,460.07 net** after modeled costs.

The largest within-trade peak-to-trough gross MTM swing was **₹29,113.50** on the same trade.

This means terminal P&L alone materially understates interim capital and margin pressure.

## Structural payoff inference
Let the 10:00 entry ATM strike be A, with 50-point spacing. The strategy uses:
- CE long at A+800 and two CE shorts at A+850.
- PE long at A-800 and two PE shorts at A-850.

Ignoring premiums and transaction costs, each side behaves like a ratio spread. On the call side, expiry payoff is:
- 0 for S <= A+800,
- S-(A+800) for A+800 < S <= A+850,
- A+900-S for S > A+850.

The put side is symmetric:
- 0 for S >= A-800,
- A-800-S for A-850 <= S < A-800,
- S-(A-900) for S < A-850.

Therefore the terminal payoff can become negative once NIFTY moves beyond approximately **A±900**. The observed 100% terminal win rate is consistent with the accepted sample's expiries not finishing far enough into the unbounded-loss tails after accounting for the positive entry credit; it does not establish that the ratio structure has bounded downside.

## Brokerage sensitivity
The baseline run uses ₹20 brokerage per executed order for historical consistency. A separate sensitivity using ₹10 per executed order, while keeping all other modeled costs unchanged, raises aggregate net P&L from ₹84,698.69 to approximately **₹88,757.89**. This sensitivity is included because Paytm Money's current F&O FAQ and an official pricing announcement present different brokerage figures; the historical baseline was not silently changed.

## Interpretation
The accepted historical sample shows a strong positive realized P&L profile after the modeled costs, but the data also show large transient mark-to-market losses on every accepted trade. The most important empirical feature is therefore **positive terminal expectancy paired with substantial path risk**, not the terminal win rate alone.

The data-quality result is equally important. Because nearly half of candidate expiries were excluded and most exclusions were missing entry legs, the study cannot be interpreted as a complete weekly-history backtest. Selection effects from source availability may materially affect the observed distribution.

The 2026 results are much larger than 2025. That difference is descriptive and may reflect market volatility/regime effects, but this phase does not fit a formal regime model.

## Strengths
- Exact user-specified four-leg quantities.
- Trading-day, not calendar-day, entry selection.
- Same-minute look-ahead avoided by using the 10:00 spot open for strike selection.
- 1-minute option execution proxies.
- Explicit slippage and brokerage.
- Date-aware transaction-cost model.
- Historical lot-size change incorporated.
- Complete trade ledger retained.
- Source gaps explicitly logged rather than silently imputed.
- Path-risk MTM retained in the ledger.

## Limitations
- Bid/ask spreads and queue position are not reconstructed from historical order-book data.
- Slippage is a fixed parameter, not a liquidity-conditioned model.
- The available option source does not provide a complete weekly history for every candidate expiry/required strike.
- No capital or broker margin model is included, so the large negative MTM episodes are not translated into required cash/margin.
- The confidence interval for the mean treats trades as independent.
- No out-of-sample forward period exists inside this phase beyond the bounded historical sample.
- No alternative strike distances, entry times or exit rules are compared here; doing so requires a new phase.

## Conclusion
Within the **43 complete historical trades** that could be reconstructed under the frozen specification, the strategy produced **₹84,698.69 net P&L after modeled costs**, with a **₹1,969.74 mean net P&L per accepted trade** and no terminal net losses.

The strongest caution is that every accepted trade experienced negative intratrade gross MTM, with a worst observed trough of **-₹24,394.50** and a maximum peak-to-trough swing of **₹29,113.50**. The result therefore should be treated as a ratio-spread strategy with potentially high interim capital/margin requirements rather than as a low-risk 100%-win system.

No trading recommendation is made from this descriptive backtest alone.

## Next research direction
The next phase should focus on:
1. margin/capital requirements and capital-adjusted return,
2. liquidity-aware bid/ask and slippage modeling,
3. regime-conditioned performance,
4. robustness across nearby OTM distances and entry times,
5. true walk-forward out-of-sample validation,
6. comparison with the frozen V2/V3 baselines under identical cost assumptions.
