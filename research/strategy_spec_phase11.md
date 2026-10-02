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
