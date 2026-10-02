# Final Stand v4

## Research Status
- Phase 0 — Strategy specification: **IN PROGRESS**
- Current strategy revision: **V2 — dynamic OTM8 re-centering**
- Backtest: **NOT YET RUN**
- Data validation: **PENDING**

## Current Research Files
- [Strategy V2 specification](research/strategy_spec_v2.md)
- [Research status](research/research_status.md)
- [Error log](logs/error_log.md)
- [Decision/conversation log](logs/decision_log.md)

## Important
This repository records the agreed research specification and implementation decisions. Hidden chain-of-thought is not stored; decision summaries and user-provided requirements are recorded instead.


## Phase 11 — Premium Direction Predictor (research branch)

- Branch: [phase-11-premium-direction-predictor](https://github.com/vishnuvcr/Final-Stand-v4/tree/phase-11-premium-direction-predictor)
- [Phase 11 research plan](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-11-premium-direction-predictor/research/research_plan_phase11.md)
- [Phase 11 research status](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-11-premium-direction-predictor/research/research_status_phase11.md)
- [Premium combination search](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-11-premium-direction-predictor/results/phase11_premium_combination_search.md)
- [Robustness/falsification report](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-11-premium-direction-predictor/results/phase11_robustness.md)
- [Phase 11 decision log](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-11-premium-direction-predictor/logs/decision_log_phase11.md)
- [Phase 11 error log](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-11-premium-direction-predictor/logs/error_log_phase11.md)

**Latest Phase 11 inference (2026-10-02):** two frozen relative call-wing premium ratios reach 60% (12/20) on the 2026 chronological holdout, but the holdout's always-bearish baseline is 65%, the two ratios make identical classifications in the holdout, and performance falls from 62.35% before the September 2025 expiry-convention boundary to 52.78% afterward. The result remains a research lead only; no trading strategy has been authorized.


## Phase 12 — Full-Chain Option Surface + OI Direction Research

A new research branch expands the Phase 11 search beyond OTM6/7/8 to the **full available NIFTY option chain**, including all strikes, option premiums, open interest and volume at 4-DTE/10:00 IST.

- [Phase 12 branch](https://github.com/vishnuvcr/Final-Stand-v4/tree/phase-12-full-chain-oi-direction)
- [Phase 12 research plan](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-12-full-chain-oi-direction/research/research_plan_phase12.md)
- [Phase 12 status](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-12-full-chain-oi-direction/research/research_status_phase12.md)
- [Phase 12 workflow](https://github.com/vishnuvcr/Final-Stand-v4/blob/phase-12-full-chain-oi-direction/.github/workflows/phase-12-full-chain-oi-direction.yml)

**Phase 12 status:** implementation complete; empirical GitHub Actions execution pending/completing. No trading conclusion has been drawn.
