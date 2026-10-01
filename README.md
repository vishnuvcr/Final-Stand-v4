# Final Stand v4

## Research Status
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
