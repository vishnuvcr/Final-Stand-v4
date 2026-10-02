# Final Stand v4

## Research Status
- Phase 0–5 baseline research: **COMPLETED / FROZEN**
- Phase 6 V3 static OTM8 reversal: **COMPLETED / FROZEN**
- Phase 7 V4 double-sided OTM16/17: **COMPLETED / FROZEN**
- Phase 8 option-data source recovery: **COMPLETED AS A SEPARATE RECOVERY TRACK**
- Phase 9 credit-selected OTM6/7/8: **COMPLETED — reproducible archive verified 2026-10-02**
- Phase 10 robustness/context analysis: **IN CLOSURE — computational robustness complete; Cartesian cost/context acquisition running**

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
- Net P&L: ₹84,698.69
- Mean net/trade: ₹1,969.74
- Median net/trade: ₹733.62
- Worst terminal net trade: ₹38.27
- Best terminal net trade: ₹16,743.46
- Worst intratrade gross MTM: -₹24,394.50
- Largest peak-to-trough gross MTM swing: ₹29,113.50

The V4 result remains frozen and is not modified by Phase 9 or Phase 10.

## Research control files
- [Project operating protocol](research/project_operating_protocol.md)
- [Master research plan](research/research_plan.md)
- [Decision/conversation log](logs/decision_log.md)
- [Error log](logs/error_log.md)
- [Research status](research/research_status.md)

## Phase 9 — Credit-Selected OTM6/7/8
Rule:
- At 10:00, calculate PE7 + PE8 - PE6 and CE7 + CE8 - CE6.
- Select the higher positive credit.
- Enter the corresponding 1:-1:-1 OTM6/7/8 structure.
- Target 90% of the initial net-credit flatline.
- If not reached, exit at 0 DTE/15:29.
- Stop grid was frozen in advance and selected only on validation.

Frozen implementation:
- Historical nearest listed expiry from contract data.
- 50-point ATM/strike mapping with midpoint ties upward.
- Historical lot size: 75 through 30-Dec-2025 expiry; 65 thereafter.
- 0.10 premium-point slippage per option execution.
- ₹10 brokerage per unique F&O order plus date-aware exchange/SEBI/STT/stamp/GST charges.
- No missing-leg imputation, reversal, roll, or dynamic OTM8 re-centering.

### Phase 9 reproducible result
- GitHub Actions run: **36970175719 — SUCCESS**
- Output commit: **d03d7a1**
- Executable trades: **56**
- Skipped candidates: **26**
- Validation-selected stop: **0x / no stop**
- Untouched test: **12 trades**
- Test mean net P&L: **₹1,626.73/trade**
- Test median net P&L: **₹2,646.34**
- Test total net P&L: **₹19,520.73**
- Test win rate: **91.67%**
- Test profit factor: **2.22**
- Target hit rate: **91.67%**
- Expiry fallback: **8.33%**
- Selection: **75% puts / 25% calls**
- Bootstrap 95% CI for test mean: **₹-1,946 to ₹3,869**

Interpretation: the realized untouched test is positive, but the test contains only 12 trades and its bootstrap interval includes zero. This is not sufficient to establish a stable out-of-sample edge. Phase 10 therefore tests robustness rather than changing the Phase 9 rule.

### Phase 9 outputs
- [Specification](research/strategy_spec_v5_credit_selected.md)
- [Research plan](research/research_plan_v5_credit_selected.md)
- [Data manifest](research/data_manifest_v5.json)
- [Backtest engine](scripts/backtest_v5_credit_selected.py)
- [Stop/analysis engine](scripts/select_v5_stop_and_analyze.py)
- [Workflow](.github/workflows/phase-9-credit-selected-otm6-8.yml)
- [Final summary](results/strategy_v5_final_summary.json)
- [Full trade ledger](results/strategy_v5_trades.csv)
- [Untouched test ledger](results/strategy_v5_test_trades.csv)
- [Stop validation](results/strategy_v5_stop_selection.csv)
- [Full-sample stop sensitivity](results/strategy_v5_stop_full_sample_sensitivity.csv)
- [Target sensitivity](results/strategy_v5_target_sensitivity.csv)
- [Data quality](results/strategy_v5_data_quality.json)
- [Selection metadata](results/strategy_v5_selection_meta.json)

## Phase 10 — Robustness and Context Analysis
Phase 10 will use a separate branch and will not alter Phase 9 frozen outputs.

Pre-specified work:
1. Re-run the frozen Phase 9 strategy across target fractions 85%, 90%, 95%, 100%.
2. Stress slippage at 0.00, 0.10, 0.25 and 0.50 premium points.
3. Stress brokerage/transaction costs using documented date-aware schedules.
4. Report call-versus-put selection and selection-margin distributions without changing the selection rule.
5. Evaluate chronological/yearly/quarterly stability where sample coverage permits.
6. Evaluate drawdown/path risk and capital requirements, including intratrade MTM rather than terminal P&L alone.
7. Add pre-specified market-context analysis where validated data are available: India VIX/volatility, FII/DII, major global indices, USDINR, gold, corporate actions and relevant news/regime indicators.
8. Preserve all data provenance and cache expensive source files.
9. Log every failure and update research status after each workflow step.
10. Do not optimize parameters on the untouched test set.

Phase 10 stopping rule: complete the predefined robustness/context grid once, then freeze the findings and proceed to the final manuscript rather than opening an unbounded parameter search.

## Manuscript requirement
The final research phase will produce a structured manuscript with research questions, aims/objectives, methodology, data/provenance, statistical analysis, results, inference, discussion, strengths, limitations, conclusion, future research, figures, tables, appendices and supplementary material.

## Frozen-phase policy
Any new strike distance, target, stop, selection rule, regime filter, capital model or execution assumption must be introduced as a new phase and branch. Existing phase outputs are not overwritten.


### Phase 10 current closure state
- Computational robustness run 36971887518: **SUCCESS**.
- 56 executable trades in the Phase 10 baseline.
- Target sensitivity and single-factor cost sensitivity persisted.
- Closure correction: full 4×3 slippage/brokerage Cartesian stress and market-context acquisition are now being executed before Phase 10 is frozen.
- Official context sources include NSE historical India VIX, historical NIFTY/index data and FII/FPI/DII reports; these sources describe the available historical series and note that FII/FPI data are provisional. The context analysis will not create a new trading filter.
