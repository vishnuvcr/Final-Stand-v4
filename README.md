# Final Stand v4

## Research Status
- Phase 0 — Strategy specification: **COMPLETED**
- Current strategy revision: **V2 — dynamic OTM8 re-centering**
- Backtest: **RESEARCH PHASES 0–5 COMPLETED**
- Data validation: **COMPLETED FOR AVAILABLE SAMPLE; COVERAGE LIMITATION DOCUMENTED**

## Current Research Files
- [Strategy V2 specification](research/strategy_spec_v2.md)
- [Research status](research/research_status.md)
- [Error log](logs/error_log.md)
- [Decision/conversation log](logs/decision_log.md)

## Important
This repository records the agreed research specification and implementation decisions. Hidden chain-of-thought is not stored; decision summaries and user-provided requirements are recorded instead.

## Research plan and methodology
- [Master research plan](research/research_plan.md)
- [Backtest methodology](research/backtest_methodology_v1.md)
- [Data-source register](research/data_sources.md)
- [Manuscript scaffold](manuscript/README.md)
- [Phase 1 workflow](.github/workflows/phase-1-data-validation.yml)

## Phase 1 checkpoint
Unit tests have passed. The corrected 2025–2026 candidate backtest completed successfully. The validated empirical sample contains 84 trades (42 CE, 42 PE); many earlier 2025 expiries are unavailable in the selected intraday option source and are excluded rather than imputed. The engine uses predicate-pushed Parquet reads, historically applicable NIFTY lot sizes, and next-minute execution after target/trigger observations.

## Latest Phase 1 outputs
- [Trade results](results/trades.csv)
- [Call/put summary](results/summary.csv)
- [Data-quality record](results/data_quality.json)

## Phase 3 sensitivity output
- [Robustness grid](results/phase3_sensitivity.csv)


## Final research status
- Phase 0: completed.
- Phase 1: corrected data/backtest completed.
- Phase 2: engine validation completed.
- Phase 3: robustness grid completed.
- Phase 4: statistical analysis completed.
- Phase 5: manuscript and conclusion completed.

## Final manuscript
- [Complete research manuscript](manuscript/final_research_manuscript.md)
- [Research status and phase log](research/research_status.md)
- [Robustness grid](results/phase3_sensitivity.csv)
- [Statistical results](results/statistics.csv)
- [CE/PE tests](results/call_put_tests.csv)
- [Trade ledger](results/trades.csv)
- [Data-quality record](results/data_quality.json)

**Stopping rule:** the predefined computational research phases are complete. Further work is future research and will not be silently mixed into the completed baseline.
