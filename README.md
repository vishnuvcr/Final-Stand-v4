# Final Stand v4

## Research Status
- Phase 0 — Strategy specification: **COMPLETED**
- Current strategy revision: **V2 — dynamic OTM8 re-centering**
- Backtest: **PHASE 1 COMPLETED — PRELIMINARY RESULTS**
- Data validation: **PARTIAL — COVERAGE LIMITATION DOCUMENTED**

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
