# Decision / Conversation Log — Phase 11

## 2026-10-02 — New research requested

User requested a separate research branch to test whether the following 4-DTE NIFTY option premium construction can predict the direction from the observation spot to weekly expiry:

- Call calculation = OTM7 call premium + OTM8 call premium − OTM6 call premium.
- Put calculation = OTM7 put premium + OTM8 put premium − OTM6 put premium.
- If call calculation > put calculation → predict bearish.
- If put calculation > call calculation → predict bullish.

### Decisions recorded

1. New branch: `phase-11-premium-direction-predictor`.
2. Primary formula and directional mapping are frozen exactly as supplied.
3. Observation timestamp inherits the project's established 4-DTE / 10:00 IST convention.
4. Outcome is NIFTY expiry settlement versus the 10:00 entry spot.
5. Equality is a neutral/tie observation, not forced into either direction.
6. The primary study is predictive/statistical first; a trading implementation is a later phase.
7. Historical expiry-calendar rules are date-aware. NSE revised NIFTY weekly expiry from Thursday to Tuesday for new contracts from September 2025 onward.
8. Cost modelling must include slippage and applicable Paytm Money brokerage/statutory/exchange charges if a trading implementation is reached.
9. The inverse label mapping will be tested only as a diagnostic, not silently substituted for the user's primary rule.

Hidden chain-of-thought is not stored. This log stores requirements and implementation decisions.
