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