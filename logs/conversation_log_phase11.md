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


## 2026-10-02 — Research progress checkpoint

- Source review identified a primary intraday option candidate (Hugging Face) and an independent NIFTY 1-minute spot dataset (GitHub).
- Implemented the predictor formula and exact user-specified directional mapping.
- Implemented a 4-DTE event builder using the 10:00 bar OPEN to avoid look-ahead.
- Added manual GitHub Actions validation/acquisition/build workflow.
- No historical performance result has been generated yet.


## 2026-10-02 — Workflow execution and empirical checkpoint

User instructed: “Ok proceed” and supplied a GitHub Actions screenshot showing repeated failed Phase 11 runs.

Actions taken:
1. Accessed the actual Phase 11 check-run/job logs rather than relying on the screenshot alone.
2. Diagnosed and fixed the initial `ModuleNotFoundError: No module named 'scripts'`.
3. Confirmed 8/8 unit tests passed after adding Python package markers and `PYTHONPATH`.
4. Diagnosed and fixed the invalid Actions cache key containing commas.
5. Successfully acquired the TradeMarkk primary archive plus Rissin/Upstox secondary archive and built 121 valid events from 132 expiry candidates.
6. Ran the primary statistical analysis and chronological 2026 holdout.
7. Added an independent secondary-source audit. The first implementation caused runner shutdown through excessive memory usage; the audit was rewritten as a streaming/vectorized year-by-year comparison.
8. Final successful Phase 11 workflow run completed acquisition, reused the event dataset, completed the independent source audit, completed statistical analysis, and committed outputs.
9. Current decision: do not promote the directional predictor to trading translation; continue with Phase 5 robustness/falsification.

Only decision summaries and user-visible requirements are recorded here; hidden chain-of-thought is not stored.
