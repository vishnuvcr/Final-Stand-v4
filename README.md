# Final Stand v4

## Research Status
- Phase 0 — Strategy specification: **COMPLETED**
- Current research strategy revision: **V3 — static OTM8 reversal hedge** (V2 remains the frozen prior baseline)
- Backtest: **PHASES 0–5 COMPLETED; PHASE 6 V3 COMPLETED**
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


## Phase 6 — Strategy V3 restart
- **IN PROGRESS** on branch `phase-6-reversal-otm8`.
- Strategy 1: long OTM6 PE, short OTM7 PE, short OTM8 PE; static OTM8 trigger; on breach, buy back OTM8 PE and sell the opposite CE at the same initial OTM8 strike.
- Strategy 2: long OTM6 CE, short OTM7 CE, short OTM8 CE; static OTM8 trigger; on breach, buy back OTM8 CE and sell the opposite PE at the same initial OTM8 strike.
- No profit target; exit at expiry using the frozen 15:29 bar-open convention.
- [Strategy V3 specification](research/strategy_spec_v3.md)
- [Phase 6 workflow](.github/workflows/phase-6-reversal-otm8.yml)


## Phase 6 — Strategy V3
- [Strategy V3 specification](research/strategy_spec_v3.md)
- [V3 trade ledger](results/strategy_v3_trades.csv)
- [V3 summary](results/strategy_v3_summary.csv)
- [V3 statistics](results/strategy_v3_statistics.csv)
- [V3 call/put comparison](results/strategy_v3_call_put_comparison.csv)
- [V3 statistical tests](results/strategy_v3_call_put_tests.csv)
- [V3 data quality](results/strategy_v3_data_quality.json)


## Phase 6 — V3 final result
- **COMPLETED** on branch `phase-6-reversal-otm8`.
- Strategy 1 (Put): 42 trades; total net P&L ₹-58,006.84; mean ₹-1,381.12; win rate 83.33%; profit factor 0.50; roll rate 21.43%.
- Strategy 2 (Call): 42 trades; total net P&L ₹29,527.08; mean ₹703.03; win rate 69.05%; profit factor 2.71; roll rate 9.52%.
- Call-vs-put tests: Mann–Whitney p=0.9893; paired sign-permutation p=0.2704.
- The result is descriptive for the validated available sample; the 2025–2026 option dataset has the same coverage limitations documented in the data-quality record.
