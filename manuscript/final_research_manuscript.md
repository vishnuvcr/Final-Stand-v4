# Final Stand v4 — Research Manuscript

## Abstract

This study evaluates Strategy V2, a defined NIFTY 50 index-option structure using an initial OTM6/OTM7/OTM8 construction and dynamic current-spot OTM8 re-centering, over the validated portion of 2025–2026 for which one-minute option data were available. The research uses a reproducible Python/GitHub Actions pipeline, historical NIFTY spot data, one-minute option data, explicit execution slippage, brokerage, exchange charges, SEBI turnover fees, stamp duty and date-aware STT. The validated empirical sample contains 84 trades, equally divided between CE and PE variants. Under the baseline scenario, CE trades had mean net P&L ₹189.35 and total net P&L ₹7,952.82; PE trades had mean net P&L -₹1,231.88 and total net P&L -₹51,739.07. Bootstrap intervals for the mean include zero for both variants. The paired CE-vs-PE sign-permutation test gave p=0.1444 and the Mann–Whitney test p=0.6579. These results are descriptive and do not establish future profitability. The principal limitation is data coverage: many candidate expiries are unavailable in the selected historical intraday option source, so missing observations were excluded rather than imputed.

## 1. Research questions
1. Can Strategy V2 be implemented without look-ahead bias under one-minute historical data?
2. How does the observed net P&L distribution behave after realistic execution and statutory costs?
3. How sensitive are results to target level and option-premium slippage?
4. Does the observed CE/PE difference survive non-parametric statistical testing?
5. Which data-quality, execution and model assumptions remain material threats to inference?

## 2. Aims and objectives
Primary aim: scientifically evaluate the reproducible historical performance characteristics of Strategy V2 under documented execution-cost assumptions.

Objectives: freeze the strategy before performance analysis; use historically appropriate expiry dates and lot sizes; use the actual 10:00 entry spot; execute target/roll actions on the next available minute; model brokerage, exchange charges, SEBI turnover fee, stamp duty, STT and slippage; preserve cached data; run a predefined robustness grid; and produce reproducible outputs.

## 3. Literature review
Option backtests can be materially affected by trading costs, particularly bid–ask spreads. Research on listed options has shown that apparent abnormal returns can disappear after trading costs are incorporated. More recent index-option microstructure work separates price impact and bid–ask spread components and finds that option trades can affect the underlying and volatility, while the economic magnitude of those effects is small.

Backtest overfitting is another central methodological concern. Bailey et al. show that trying multiple configurations can generate apparently strong historical performance through selection effects. This project therefore freezes its baseline before the robustness grid and reports the tested scenarios rather than selecting a preferred configuration after observing results.

Indian derivatives participation provides important context but is not direct evidence about this strategy. SEBI's FY22–FY24 study reported substantial aggregate losses among individual F&O traders, and SEBI's 2026 research catalogue includes updated FY25–FY26 studies of derivatives trading behaviour and profitability.

Sources:
- https://www.sciencedirect.com/science/article/pii/0304405X80900161
- https://www.sciencedirect.com/science/article/pii/S1386418121000550
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2308659
- https://www.sebi.gov.in/reports-and-statistics/research/sep-2024/study-analysis-of-profits-and-losses-in-the-equity-derivatives-segment-fy22-fy24-_86905.html
- https://www.sebi.gov.in/reports-and-statistics/research/aug-2026/study-trading-behaviour-of-individual-traders-in-the-equity-derivatives-segment-fy25-fy26-_103836.html

## 4. Data sources and provenance
The implementation uses cached NIFTY one-minute spot data, one-minute NIFTY option data from the configured Hugging Face source, and NSE/SEBI published contract and levy information. Missing option observations are recorded in results/data_quality.json and excluded rather than imputed.

NSE's current NIFTY specification documents Tuesday expiry and previous-trading-day adjustment for Tuesday holidays and publishes strike-interval rules. Historical rules are treated as date-dependent.

Source: https://www.nseindia.com/static/products-services/equity-derivatives-nifty50

## 5. Strategy and methodology
Entry is defined at 10:00. Initial legs use OTM6/OTM7/OTM8 strikes. A breach of the OTM8 trigger causes a next-minute adjustment. The replacement short option is re-centred to current-spot OTM8. Profit-target observation also executes on the next available minute, avoiding same-bar look-ahead. Positions remaining at expiry use the final available quote or intrinsic value when a quote is unavailable.

The study is retrospective and computational. Every trade records entry, exit, order count, rolls, fees, peak mark-to-market and trough mark-to-market.

## 6. Transaction-cost model
Baseline: Paytm Money F&O brokerage ₹20 per executed order; slippage ₹0.10 premium points per execution; NSE option transaction charge ₹35.03 per lakh of premium value from 1-Oct-2024 with the March-2026 revision to ₹35.53 per lakh-equivalent rate; SEBI turnover fee ₹10 per crore; equity-option stamp duty 0.003% on the buyer; STT on option sales 0.10% through 31-Mar-2026 and 0.15% from 1-Apr-2026; GST 18% on applicable service components.

Sources:
- https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web
- https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax
- https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies
- https://nsearchives.nseindia.com/content/circulars/FA64232.pdf
- https://nsearchives.nseindia.com/content/circulars/FA73061.pdf

These are published-rate assumptions, not broker-generated historical contract-note reconstruction. Platform-specific incidental fees may differ.

## 7. Statistical analysis
For each variant: trade count, mean, median, win rate, profit factor, total P&L, standard deviation, maximum observed loss, bootstrap 95% confidence interval, target-hit rate, expiry-exit rate, roll frequency and order count.

For CE/PE comparison: Mann–Whitney U and paired sign-permutation tests. The tests are inferential summaries only; the small and incomplete sample limits power.

## 8. Results
| Metric | CE | PE |
|---|---:|---:|
| Trades | 42 | 42 |
| Mean net P&L | ₹189.35 | -₹1,231.88 |
| Median net P&L | ₹270.38 | ₹250.53 |
| Profitable trades | 71.43% | 78.57% |
| Profit factor | 1.31 | 0.36 |
| Total net P&L | ₹7,952.82 | -₹51,739.07 |
| Std. dev. | ₹3,319.70 | ₹5,074.36 |
| Worst observed trade | -₹17,684.58 | -₹19,582.24 |
| Bootstrap 95% CI for mean | -₹957.14 to ₹1,029.24 | -₹2,842.04 to ₹164.79 |
| Target hit | 92.86% | 78.57% |
| Expiry exit | 7.14% | 21.43% |
| Average rolls | 0.048 | 0.190 |

CE-minus-PE paired mean difference was ₹1,421.24 per aligned expiry. Mann–Whitney p=0.6579; paired sign-permutation p=0.1444.

## 9. Robustness
The predefined grid varied target fraction (90%, 95%, 100%) and slippage (0.00, 0.10, 0.25 points). The complete table is results/phase3_sensitivity.csv. In the tested sample, aggregate CE net P&L remained positive across the grid while aggregate PE net P&L remained negative. Increasing slippage reduced CE aggregate P&L and made PE aggregate P&L more negative.

These are historical sample observations, not forecasts.

## 10. Discussion
The corrected implementation demonstrates that target-hit frequency alone is not a sufficient performance measure. A strategy can hit a target frequently while a small number of large expiry losses dominate aggregate P&L. This effect is particularly visible in the PE sample, where the median trade is positive but the mean and aggregate result are negative.

The explicit cost model is important because option trading costs can materially change apparent strategy performance. The statistical tests do not provide conventional evidence of a CE/PE difference at the 5% level, and incomplete historical option coverage further limits inference.

## 11. Strengths
1. Frozen strategy specification before robustness testing.
2. Separate version-controlled phase branches.
3. Manually triggerable GitHub Actions workflows.
4. Cached data strategy.
5. Explicit data-quality skip ledger.
6. Next-minute execution controls against look-ahead.
7. Historical lot-size treatment.
8. Date-aware transaction costs.
9. Bootstrap and non-parametric inference.
10. Predefined sensitivity grid.

## 12. Limitations
1. The selected one-minute option dataset does not cover every candidate expiry.
2. Bid/ask/depth data are unavailable, so premium-point slippage is a proxy.
3. Broker contract notes are unavailable.
4. Only 42 observations per side are currently usable.
5. Retrospective backtests remain vulnerable to data-mining and regime dependence.
6. No untouched live/paper-trading validation has been performed.
7. FII/DII flows, global crossing inefficiencies, news, volatility regimes, India VIX, gold and other exogenous variables are not yet predictive conditioning variables.
8. Historical NSE contract archives should be used to independently validate every candidate expiry and strike regime before publication-grade claims.

## 13. Conclusion
The project now has a reproducible corrected implementation, explicit cost accounting, robustness analysis and statistical reporting. The available historical sample shows different aggregate P&L characteristics for the CE and PE variants, but the confidence intervals are wide, the sample is incomplete and the CE/PE tests are not statistically significant at conventional thresholds. The results therefore constitute a research finding requiring independent validation rather than proof of a persistent trading edge.

No live-trading decision should be based on this backtest alone.

## 14. Future research
1. Acquire complete NSE contract-wise intraday option history for every candidate expiry.
2. Replace proxy slippage with bid/ask and depth-of-book execution.
3. Validate every historical transaction-charge regime against dated circulars.
4. Add volatility/regime conditioning.
5. Add FII/DII flows, India VIX, global index futures, USDINR and gold.
6. Add event/news filters without modifying the frozen baseline.
7. Run strict walk-forward validation with an untouched holdout.
8. Model margin, capital usage and drawdown.
9. Test alternative exits only in nested validation.
10. Conduct paper trading using broker execution logs before any live deployment.

## 15. Reproducibility and appendices
Primary outputs: results/trades.csv, results/summary.csv, results/statistics.csv, results/call_put_tests.csv, results/phase3_sensitivity.csv, results/data_quality.json, results/equity_CE.png, results/equity_PE.png, results/pnl_distribution.png.

Research phases: Phase 0 strategy specification; Phase 1 data validation and corrected baseline; Phase 2 engine validation; Phase 3 robustness grid; Phase 4 statistical analysis; Phase 5 manuscript and conclusion.

A positive historical aggregate result is not sufficient to establish a persistent exploitable market inefficiency; future claims require independent out-of-sample and execution validation.