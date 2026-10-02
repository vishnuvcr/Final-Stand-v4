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


## Phase 11 — Premium Direction Predictor

- Branch: [phase-11-premium-direction-predictor](https://github.com/vishnuvcr/Final-Stand-v4/tree/phase-11-premium-direction-predictor)
- [Research plan](research/research_plan_phase11.md)
- [Specification](research/strategy_spec_phase11.md)
- [Literature review](research/literature_review_phase11.md)
- [Data manifest](research/data_manifest_phase11.json)
- [Data source assessment](research/data_sources_phase11.md)
- [Signal engine](scripts/phase11/signal.py)
- [Event builder](scripts/phase11/build_events.py)
- [Unit tests](tests/phase11/test_signal.py)
- [Research status](research/research_status_phase11.md)
- [Decision log](logs/decision_log_phase11.md)
- [Error log](logs/error_log_phase11.md)
- [Conversation/decision summary](logs/conversation_log_phase11.md)
- [Manual workflow](.github/workflows/phase-11-premium-direction-predictor.yml)

**Phase 11 status:** Phase 3/4 completed; Phase 5 robustness/falsification in progress. 121 valid events were tested. Primary directional accuracy is 50.41% (61/121); 2026 holdout accuracy is 45.0% (9/20). No trading translation has been authorized.


### Phase 11 current results
- [Statistical analysis](results/phase11_statistical_analysis.md)
- [Statistical analysis JSON](results/phase11_statistical_analysis.json)
- [Independent source audit](results/phase11_cross_source_audit.json)
- [Event dataset](results/phase11_events.csv)
- [Research status](research/research_status_phase11.md)
- [Decision log](logs/decision_log_phase11.md)
- [Error log](logs/error_log_phase11.md)

**Current scientific inference:** the pre-specified premium-direction mapping does not demonstrate stable out-of-sample directional predictive power. The isolated overall Pearson spread/return association is treated as exploratory because it is not supported by the rank/logistic tests or the 2026 chronological holdout. Phase 5 robustness/falsification remains before any trading translation.


### Phase 11 current results — premium combinations
- [Premium combination search](results/phase11_premium_combination_search.md)
- [Premium combination search JSON](results/phase11_premium_combination_search.json)

The leading research signal is a relative call-wing ratio: CE OTM6/OTM7 and CE OTM6/OTM8 log-ratios each reached 59.41% on development and 12/20 (60%) on the 2026 holdout. The 5,000-permutation maximum-threshold-accuracy diagnostic gave p=0.5118, and the holdout has only 20 observations. No trading strategy is authorized from this result. Phase 5 robustness/falsification will now freeze these candidates and test them chronologically, by regime/liquidity, and on the independent source.


### Phase 11 robustness status
- [Frozen-candidate robustness report](results/phase11_robustness.md)
- [Frozen-candidate robustness JSON](results/phase11_robustness.json)

**Phase 5 status:** IN PROGRESS. The two call-wing ratio candidates show 60% on the 20-event 2026 holdout but do not beat the 65% always-bearish baseline and weaken after the September 2025 expiry-convention boundary. No trading translation is authorized.
