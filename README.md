# Final Stand v4

## Research Status
- Phase 8 option-data source recovery: **IN PROGRESS — SOURCE DISCOVERY COMPLETE; ACQUISITION PENDING**
- [Phase 8 source audit](research/phase8_data_source_audit.md)
- Phase 0–5 baseline research: **COMPLETED**
- Phase 6 V3 static OTM8 reversal: **COMPLETED**
- Phase 7 V4 double-sided OTM16/17: **COMPLETED**

## Phase 7 V4 — Final Backtest Result
Strategy:
- Buy 1 OTM16 Call
- Sell 2 OTM17 Call
- Buy 1 OTM16 Put
- Sell 2 OTM17 Put
- Enter 4 trading days before expiry at 10:00 IST
- Use the 10:00 NIFTY spot open for strike selection
- Exit at 0 DTE using the 15:29 IST option-bar-open convention

Accepted sample:
- 92 candidate expiries
- 43 complete trades
- 49 skipped candidates
- Terminal win rate: 43/43 = 100%
- Gross P&L: ₹93,250.35
- Modeled costs: ₹8,551.66
- Net P&L: **₹84,698.69**
- Mean net/trade: ₹1,969.74
- Median net/trade: ₹733.62
- Worst terminal net trade: ₹38.27
- Best terminal net trade: ₹16,743.46
- Worst intratrade gross MTM: **-₹24,394.50**
- Largest peak-to-trough gross MTM swing: **₹29,113.50**

Important interpretation: the 100% terminal win rate did not imply low path risk. All 43 accepted trades experienced negative intratrade gross MTM. The usable historical coverage was 46.74%, primarily because required entry option legs were unavailable for many candidate expiries.

## Research control files
- [Project operating protocol](research/project_operating_protocol.md)
- [Master research plan](research/research_plan.md)
- [V4 strategy specification](research/strategy_spec_v4.md)
- [V4 research status](research/research_status_v4.md)
- [V4 results and interpretation](research/phase7_results_interpretation.md)
- [V4 research manuscript](manuscript/strategy_v4_manuscript.md)
- [Decision/conversation log](logs/decision_log.md)
- [Error log](logs/error_log.md)

## V4 implementation
- [V4 backtest engine](scripts/backtest_v4.py)
- [V4 analysis](scripts/analyze_v4.py)
- [V4 unit tests](tests/test_v4_strategy.py)
- [V4 GitHub Actions workflow](.github/workflows/phase-7-double-sided-otm16-17.yml)

## V4 outputs
- [V4 trade ledger](results/strategy_v4_trades.csv)
- [V4 summary](results/strategy_v4_summary.csv)
- [V4 statistics](results/strategy_v4_statistics.csv)
- [V4 yearly results](results/strategy_v4_yearly.csv)
- [V4 monthly results](results/strategy_v4_monthly.csv)
- [V4 data-quality record](results/strategy_v4_data_quality.json)
- [V4 risk/path analysis](results/strategy_v4_risk_analysis.csv)
- [V4 Paytm Money brokerage sensitivity](results/strategy_v4_cost_sensitivity.csv)

## Prior frozen phases
### Phase 6 — V3 static OTM8 reversal
- [V3 specification](research/strategy_spec_v3.md)
- [V3 trade ledger](results/strategy_v3_trades.csv)
- [V3 summary](results/strategy_v3_summary.csv)
- [V3 statistics](results/strategy_v3_statistics.csv)
- [V3 data quality](results/strategy_v3_data_quality.json)

The V2 and V3 baselines are preserved and are not overwritten by V4.

## Stopping rule
Phase 7 is closed after specification, backtest, validation, descriptive/statistical analysis, error logging and manuscript documentation. Any new exit rule, strike-distance search, regime filter, capital model or parameter optimization requires a new phase/branch.


## Phase 8 — Option Data Source Recovery
The Phase 7 sample contains 49 skipped candidate expiries because required option observations were unavailable in the accepted source. Phase 8 is investigating independent sources before accepting that coverage limitation as final. No Phase 7 result has been changed yet.


### Phase 8B recovery outputs
- [HF recovered trade ledger](results/strategy_v4_recovered_trades_hf.csv)
- [HF recovery coverage](results/strategy_v4_recovery_coverage_hf.csv)
- [HF recovery summary](results/strategy_v4_recovery_summary_hf.json)
- [HF recovery errors](results/strategy_v4_recovery_errors_hf.json)
- [HF recovery workflow](.github/workflows/phase-8-hf-recovery.yml)


## Phase 9 — Credit-Selected OTM6/7/8
- **Status: IN PROGRESS** on branch `phase-9-credit-selected-otm6-8`.
- New rule: calculate `OTM7 + OTM8 - OTM6` for both put and call structures at 10:00, then select the higher positive credit.
- Primary profit target: 90% of the initial net-credit flatline.
- Stop-loss candidates: 0.50×, 0.75×, 1.00×, 1.25×, 1.50× of the initial net credit plus no-stop baseline.
- Stop-loss selection is chronological: development 60%, validation 20%, untouched test 20%.
- Historical expiry dates are derived from the option contract data, so the 2025 Thursday-to-Tuesday NIFTY expiry transition is not hard-coded.
- [V5 specification](research/strategy_spec_v5_credit_selected.md)
- [V5 research plan](research/research_plan_v5_credit_selected.md)
- [V5 data manifest](research/data_manifest_v5.json)
- [V5 backtest engine](scripts/backtest_v5_credit_selected.py)
- [V5 stop/analysis engine](scripts/select_v5_stop_and_analyze.py)
- [V5 workflow](.github/workflows/phase-9-credit-selected-otm6-8.yml)
