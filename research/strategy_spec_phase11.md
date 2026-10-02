# Phase 11 Specification — Premium Direction Predictor

## Core feature

For the weekly NIFTY expiry that is exactly 4 trading days away, at 10:00 IST:

**CallScore = CE(OTM7) + CE(OTM8) - CE(OTM6)**

**PutScore = PE(OTM7) + PE(OTM8) - PE(OTM6)**

**Spread = CallScore - PutScore**

## Primary directional hypothesis

The supplied hypothesis is intentionally recorded without reinterpretation:

- CallScore > PutScore → predicted NIFTY direction to expiry = **bearish**
- PutScore > CallScore → predicted NIFTY direction to expiry = **bullish**
- CallScore = PutScore → **neutral/tie**

This is a directional predictor study, not initially an option-spread trading strategy.

## Outcome

Primary realized outcome:

**ExpiryReturn = ExpirySettlement / Spot_10:00 - 1**

Direction:
- positive → bullish
- negative → bearish
- zero → neutral

A point-move version will also be stored.

## OTM definition

OTM6/7/8 are determined separately for calls and puts from the 10:00 NIFTY spot and the exchange's strike grid applicable on that date. The exact ATM rounding rule and strike interval must come from the relevant exchange specification/data and be implemented as an explicit function.

Example only:
if ATM is K and strike interval is Δ:
- OTM6 CE = K + 6Δ
- OTM7 CE = K + 7Δ
- OTM8 CE = K + 8Δ
- OTM6 PE = K − 6Δ
- OTM7 PE = K − 7Δ
- OTM8 PE = K − 8Δ

The example is conceptual; the actual ATM/strike-grid rule must be date-aware.

## Price field hierarchy

Primary:
1. reliable executable bid/ask where available.

Fallback:
2. timestamp-matched transaction/quote-derived value documented by source.

Sensitivity:
3. midpoint.

No missing quote may be silently forward-filled across material time gaps.

## Primary statistical estimands

1. Directional accuracy.
2. Balanced accuracy.
3. Probability of correct prediction conditional on non-neutral signal.
4. Continuous relation between Spread and ExpiryReturn.
5. Out-of-sample classification performance.
6. Economic magnitude of return differences across signal buckets.

## Required controls

Where obtainable:
- India VIX
- OI and volume
- IV/skew measures
- market regime
- global overnight market variables
- holiday/short-week indicators

Controls are secondary; the primary predictor remains the premium construction specified above.

## Structural calendar break

NSE changed NIFTY weekly expiry from Thursday to Tuesday for new contracts expiring from September 2025 onward. The data engine must use the historical convention applicable to each contract and must report results separately across this structural break.


## 2026-10-02 — Execution protocol clarification

### Point-in-time price field
The primary option premium is the **OPEN of the 10:00:00–10:00:59 IST one-minute bar**. Using the close of the 10:00 bar as the primary observation would introduce up to 59 seconds of post-observation information.

The NIFTY spot used in the directional outcome is likewise the **OPEN of the 10:00:00–10:00:59 IST one-minute index bar**.

The expiry value is currently a **settlement proxy** equal to the latest NIFTY 1-minute CLOSE on the expiry trading session. A later validation step must compare this against an official NSE expiry settlement field before the final manuscript labels the outcome as official settlement.

### Four-DTE calendar
The observation date is the fourth distinct NIFTY trading session immediately preceding the actual weekly expiry date. This is calendar-driven from observed NIFTY sessions, not a simple subtraction of four calendar days.

### Missing-data rule
The primary event set requires exact 10:00 option bars for all six required contracts and exact 10:00 NIFTY spot data. Missing contracts, stale timestamps, or absent bars cause an event to be excluded from the primary sample and counted in the coverage/skip report. Sensitivity analyses may later test conservative fallback prices, but they must be separately labelled.
