# Final Stand v4

## Research Status
- Phase 0–5 baseline research: **COMPLETED**
- Phase 6 V3 static OTM8 reversal: **COMPLETED**
- Phase 7 V4 double-sided OTM16/17: **BACKTEST EXECUTING**

## Current Strategy V4
- Buy 1 OTM16 Call
- Sell 2 OTM17 Call
- Buy 1 OTM16 Put
- Sell 2 OTM17 Put
- Enter 4 trading days before expiry at 10:00 IST
- Use the 10:00 NIFTY spot open for strike selection
- Exit at 0 DTE using the 15:29 IST option-bar-open convention
- Baseline slippage: INR 0.10 per premium point per execution
- Baseline brokerage: INR 20 per executed order
- Date-aware exchange, SEBI, STT, stamp-duty and GST costs included

## Research control files
- [Master research plan](research/research_plan.md)
- [V4 strategy specification](research/strategy_spec_v4.md)
- [V4 research status](research/research_status_v4.md)
- [Decision/conversation log](logs/decision_log.md)
- [Error log](logs/error_log.md)

## V4 implementation
- [V4 backtest engine](scripts/backtest_v4.py)
- [V4 analysis](scripts/analyze_v4.py)
- [V4 unit tests](tests/test_v4_strategy.py)
- [V4 GitHub Actions workflow](.github/workflows/phase-7-double-sided-otm16-17.yml)

## V4 outputs
The workflow writes:
- [V4 trade ledger](results/strategy_v4_trades.csv)
- [V4 summary](results/strategy_v4_summary.csv)
- [V4 statistics](results/strategy_v4_statistics.csv)
- [V4 yearly results](results/strategy_v4_yearly.csv)
- [V4 monthly results](results/strategy_v4_monthly.csv)
- [V4 data-quality record](results/strategy_v4_data_quality.json)

These links become populated after the GitHub Actions backtest completes. Missing historical observations are recorded as skips rather than imputed.

## Prior frozen phases
### Phase 6 — V3 static OTM8 reversal
- [V3 specification](research/strategy_spec_v3.md)
- [V3 trade ledger](results/strategy_v3_trades.csv)
- [V3 summary](results/strategy_v3_summary.csv)
- [V3 statistics](results/strategy_v3_statistics.csv)
- [V3 data quality](results/strategy_v3_data_quality.json)

The V2 and V3 baselines are preserved and are not overwritten by V4.

## Stopping rule
Phase 7 stops after specification, backtest, validation, descriptive/statistical analysis and documentation are complete. Any additional strategy or parameter exploration requires a new phase/branch.
