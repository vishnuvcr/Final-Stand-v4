# Phase 10 Source Register

## Primary exchange/regulatory sources
- NSE Historical India VIX: official historical download/report endpoint. It provides historical India VIX observations and is the primary source for volatility-context analysis.
- NSE FII/FPI & DII trading activity: official daily activity reports for NSE and combined NSE/BSE/MSEI capital-market activity. NSE notes that the data are provisional and may change after custodial confirmation.
- NSE Historical Index Data: official historical NIFTY/index data endpoint.
- NSE historical reports: official archive covering indices, India VIX, daily/monthly reports and related market statistics.
- NSE Data Sharing Policy research list: identifies historical index data, FII/FPI/DII activity, contract-wise derivatives price-volume data and derivatives archives as available research datasets.
- RBI: reference-rate documentation/source family for USD/INR context. Exact daily series will be validated before use.

## Secondary/validation sources
- Public Hugging Face/GitHub market-data repositories may be used for cross-checking where official bulk downloads are unavailable or operationally inaccessible.
- Secondary sources are never silently substituted for the accepted Phase 9 option ledger; any substitution is documented with provenance and coverage.

## Context-variable definitions
- India VIX: expected near-term volatility measure derived from NIFTY option prices; use as a descriptive volatility regime variable.
- NIFTY returns/realized volatility: calculated from validated NIFTY index observations.
- FII/DII: daily net activity, with provisional-data status retained.
- Global markets: daily returns aligned to the Indian trading date, with timezone/cutoff rules documented.
- USDINR and gold: daily observations aligned by date; no forward-looking values.
- Corporate actions/news: event-date indicators only when a reproducible timestamped source can be archived.

## Evidence collected 2026-10-02
- NSE states that India VIX represents expected NIFTY volatility over the next 30 calendar days and is calculated from NIFTY option order-book prices. See official NSE India VIX page.
- NSE provides historical India VIX downloads and historical index data through its reports interfaces.
- NSE provides FII/FPI and DII activity for NSE and combined NSE/BSE/MSEI capital-market activity and explicitly labels the data provisional.
- NSE's research-data sharing list identifies historical index data, FII/FPI/DII activity, contract-wise derivatives price-volume data and derivatives archives as research-accessible datasets.

## Search notes and limitations
- The Phase 10 analysis will not claim complete coverage until each context series is downloaded, timestamp-validated and cached.
- Web discovery establishes source availability; it does not by itself establish that a complete 2025-2026 historical extract has been acquired.
- No context variable will be used as a new entry/exit filter in Phase 10.
## Literature review — initial evidence map
- Jain, Varma & Agarwalla (Journal of Futures Markets, 2019) study Indian equity options and report that implied volatility contains information about future volatility; they characterize the market as broadly supportive of efficiency while identifying option-risk-premium features. This supports including volatility and smile/risk-premium context without assuming exploitable mispricing.
- Garg & Vipul (Journal of Futures Markets, 2015) study volatility risk premia in Indian options and report that transaction costs materially reduce the economic benefits of VRP strategies. This directly motivates the Phase 10 slippage and brokerage stress tests.
- Mutum & Das (Indian Journal of Finance, 2019) test lower-boundary conditions in NIFTY index options and report that apparent mispricing was concentrated in thinly traded and near-expiry options, while much of it was not exploitable after liquidity considerations. This motivates explicit data-availability and execution-cost controls.
- Vipul (Journal of Futures Markets, 2009) examines box-spread arbitrage efficiency in NIFTY index options using time-stamped transactions. The work is relevant to the broader market-efficiency question but does not validate the Phase 9 strategy.
- A 2026 SSRN preprint by Sumin Pillai tests several NIFTY volatility-selling strategies with explicit frictions and reports that realistic costs are important to strategy economics. It is treated as recent secondary evidence, not as established consensus.
- A 2026 SSRN preprint by Yash Agarwal analyzes NIFTY variance-risk-premium behavior using high-frequency options data and reports positive VRP on a majority of sampled days but substantial tail asymmetry and regime variation. It motivates regime/context analysis while requiring independent validation.
- A 2026 research preprint by Ashwin R. John studies NIFTY volatility-risk-premium harvesting with realistic implementation costs and a post-2024 market-structure break. It is treated as a recent preprint rather than peer-reviewed evidence.
- Broader options-market literature emphasizes the importance of liquidity, price impact, volatility state and intermediary risk premia. Phase 10 therefore reports these as explanatory/context variables rather than converting them into unvalidated trading filters.

## Literature implications for Phase 10
1. Transaction costs are a first-order robustness dimension, not an afterthought.
2. Volatility regime is relevant to option-selling economics and should be measured independently of the strategy outcome.
3. Apparent option mispricing can be concentrated in illiquid/near-expiry observations and may not be executable.
4. Recent NIFTY research is heterogeneous and includes non-peer-reviewed preprints; claims from these sources will be explicitly labeled.
5. The Phase 10 objective is robustness and explanation, not confirmation of a predetermined positive result.


## Phase 10 source validation update — 2026-10-02
Official NSE pages confirm that historical India VIX data, historical NIFTY/index data and FII/FPI/DII activity are available through NSE reporting interfaces. NSE describes India VIX as a near-term expected-volatility measure derived from NIFTY option prices and notes that FII/FPI activity data are provisional and subject to change. These series are therefore treated as context variables with provenance and missingness preserved; they are not used as new trading filters.


## Corporate-action source validation — 2026-10-02
NSE's current public Corporate Filings → Corporate Actions page exposes symbol-level purpose and ex-date/record-date fields, and NSE's research data-sharing catalogue identifies corporate-action data as a research data category. These sources are therefore retained as the authoritative source family for any reproducible corporate-action event indicator. The phase will not infer missing historical events from secondary sources. If automated acquisition fails, coverage will be reported as unavailable rather than substituted silently.


## Validated fallback source update — 2026-10-02
- The Phase 10 context repair uses the public `nseindiapy` client (v0.1.0) to access Nifty Indices historical NIFTY 50 OHLC and India VIX daily snapshots. The package documentation states that these endpoints are public and that the client auto-paginates long historical price ranges; the project source was inspected before use.
- FII/DII fallback uses the public MrChartist/FII-DII historical archive. Its documented data flow identifies NSE as the upstream source and preserves daily FII/DII net fields.
- These fallbacks are validation/recovery tooling only. The Phase 9 option ledger and Phase 10 strategy parameters are unchanged.
