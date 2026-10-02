# Conversation / Decision Summary — Phase 11

## 2026-10-02 — Research initiation

### User request
Start a separate research branch to test whether, at 4 trading days to weekly NIFTY expiry, the premium expression

- Call = OTM7 call + OTM8 call − OTM6 call
- Put = OTM7 put + OTM8 put − OTM6 put

predicts the NIFTY direction from the observation spot to expiry.

Specified mapping:
- Call calculation > Put calculation → bearish
- Put calculation > Call calculation → bullish

### Assistant actions recorded
- Checked the existing main README, research status, strategy specification, decision log, error log, workflow inventory, and existing phase branches before starting the new phase.
- Created branch `phase-11-premium-direction-predictor`.
- Initialized a detailed multi-phase research plan.
- Initialized the formal specification, status tracker, data manifest, decision log, error log, and literature review.
- Added a manual GitHub Actions workflow for protocol validation.
- Searched current NSE contract/expiry specifications and the 2025 expiry-day transition.
- Searched peer-reviewed and working-paper literature on option-implied information, skewness, call-put spreads, and subsequent returns.
- Confirmed that no performance conclusion has been made because the required historical 10:00 option dataset is not yet validated.

## Research-policy note
Only decision summaries and research records are stored here; hidden chain-of-thought is not stored.
