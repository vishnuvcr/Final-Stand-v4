# Phase 10 Research Plan — V5 Robustness and Market Context

## Purpose
Stress-test the frozen Phase 9 credit-selected OTM6/7/8 strategy without changing its selection rule, strike convention, target, stop-selection procedure, execution model, or untouched test definition.

## Research questions
1. Does the Phase 9 result persist across the pre-specified target grid of 85%, 90%, 95% and 100%?
2. How sensitive is realized net P&L to option slippage from 0.00 through 0.50 premium points?
3. How sensitive is the result to brokerage and date-aware exchange/tax charges?
4. Is performance concentrated in calls or puts, or in particular selection-margin ranges?
5. Is performance temporally stable across calendar years and quarters, subject to available observations?
6. What is the distribution of intratrade adverse MTM, terminal P&L, drawdown, time-to-target and expiry fallback?
7. How does the strategy behave across observable volatility and broader market regimes?
8. Do external context variables provide descriptive explanation without becoming post-hoc trading filters?

## Aims
- Establish robustness of the frozen Phase 9 result.
- Quantify execution-cost and path-risk sensitivity.
- Characterize temporal and side-selection stability.
- Add pre-specified market-context descriptors without optimizing a new trading rule.

## Objectives
- Reproduce the Phase 9 ledger from cached source data.
- Run the full target/slippage/cost grid.
- Produce call/put, yearly, quarterly and selection-margin summaries.
- Quantify maximum adverse excursion, drawdown, time-to-target and expiry behavior.
- Join validated context series by date where coverage is sufficient.
- Report missingness and source provenance explicitly.
- Preserve the untouched test and prohibit parameter selection from it.

## Frozen controls
- Primary Phase 9 target remains 90%.
- Primary stop remains the validation-selected 0x/no-stop rule.
- Selection remains higher positive credit between put and call structures.
- Entry remains fourth prior trading session before nearest historical listed expiry at 10:00 IST.
- No dynamic OTM8 re-centering, reversal, roll, missing-leg imputation, or new entry filter.
- No parameter is selected using the untouched test.

## Phase structure
### 10.1 Reproducibility and data audit
- Verify all Phase 9 result files and source provenance.
- Reuse cached option and spot data whenever possible.
- Record exact source revisions and file hashes.

### 10.2 Execution-cost robustness
- Target: 85%, 90%, 95%, 100%.
- Slippage: 0.00, 0.10, 0.25, 0.50 premium points per execution.
- Brokerage/cost scenarios: frozen baseline plus documented stress cases.
- Report mean, median, total P&L, win rate, profit factor, drawdown and target/expiry rates.

### 10.3 Temporal and structural stability
- Break down results by year and quarter where sample size permits.
- Report call/put counts and P&L separately.
- Bin selection margin into pre-specified quantiles for descriptive analysis only.
- Examine relationship between initial credit and realized P&L without turning it into a trading threshold.

### 10.4 Path-risk analysis
- Maximum adverse excursion.
- Maximum favorable excursion.
- Peak-to-trough equity drawdown.
- Time to target.
- Expiry fallback loss/gain distribution.
- Worst observed intratrade MTM.
- Capital-at-risk summaries under explicit assumptions.

### 10.5 Market-context analysis
Use only validated, date-aligned data. Candidate context variables:
- India VIX / volatility regime.
- NIFTY realized volatility.
- FII/DII cash-market flow where consistent historical data are available.
- Major global equity indices and overnight return proxies.
- USDINR.
- Gold benchmark.
- Relevant corporate-action dates.
- Major market/news regime indicators where reproducible historical timestamps exist.
Context variables are descriptive/explanatory. No context variable may be converted into a new trading filter in Phase 10.

## Statistical analysis
- Descriptive distributions with confidence intervals where appropriate.
- Bootstrap confidence intervals for mean and median net P&L.
- Year/quarter comparisons only when sample sizes are reported.
- Correlation/regression analyses are exploratory and will report effect sizes and uncertainty, not causal claims.
- Multiple-testing exposure will be disclosed; no exploratory context relationship will be treated as confirmatory evidence.
- The untouched test remains a final holdout and is not used to choose settings.

## Data-quality rules
- Missing context observations are reported, never silently filled.
- Option-leg gaps remain skips.
- Historical contract expiry and lot size remain date-aware.
- Transaction costs use actual execution date.
- Any new source is validated against an independent source before being treated as authoritative.

## Deliverables
- `research/phase10_research_plan.md`.
- `research/phase10_sources.md`.
- `results/phase10_robustness_grid.csv`.
- `results/phase10_cost_stress.csv`.
- `results/phase10_temporal_stability.csv`.
- `results/phase10_path_risk.csv`.
- `results/phase10_market_context.csv`.
- `results/phase10_data_quality.json`.
- Figures/tables for the eventual manuscript.
- Updated research status and error log after every execution step.

## Stopping rule
Phase 10 stops after the predefined robustness, cost, temporal, path-risk and context analyses are executed once and documented. It does not become an open-ended parameter search. Any new strategy rule requires Phase 11.

## Success criteria
Technical success requires passing tests, complete expected output files, provenance records, and remote persistence. Scientific success means the robustness envelope and limitations can be stated clearly; it does not require a positive trading result.