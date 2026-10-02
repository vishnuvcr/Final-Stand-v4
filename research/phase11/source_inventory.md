# Phase 11 — NIFTY 1-Minute Options Source Inventory

Research date: 2026-10-02

## Purpose
Identify credible public, commercial, broker, community and exchange sources for point-in-time NIFTY option premiums at 1-minute resolution.

## Tier A — strong candidates
| Source | Capability | Phase 11 status |
|---|---|---|
| OptionsData.shop | NIFTY options 1-minute full chain, every strike/expiry, OI, Parquet; advertised 2021/2026 coverage | Strong candidate; validate sample and licensing. |
| Unfluke | Full NSE F&O minute option history, every strike/expiry, NIFTY replay from 2023, Greeks | Strong candidate; validate raw export/API and timestamps. |
| ICICI Direct Breeze + breeze_options_pipeline | 1-minute NIFTY option OHLCV+OI; public bulk pipeline | Strong candidate; account/API and historical-depth validation required. |
| Shoonya Trader / Cloud Trader Pro | Free expired NIFTY option CSVs, 1-minute OHLCV+OI, all strikes claimed | Strong acquisition candidate; validate completeness. |
| MoneyTicks | 1-minute OHLC+OI for expired NIFTY contracts; API/export; archive browsable | Strong cross-check candidate; commercial access currently not open. |
| Community 1-minute archive advertised on Reddit | NIFTY 1-minute expired options, advertised 2014-2026, OHLCV+OI | Candidate only; provenance/licence must be verified. |

## Tier B — broker/API sources with limitations
| Source | Capability | Limitation |
|---|---|---|
| Zerodha Kite Connect | Historical minute candles + OI | Expired options are not continuously retrievable through normal API. |
| Upstox V3 | 1-minute historical candles from 2022 | Expired-contract depth must be tested. |
| Angel One SmartAPI | NFO 1-minute candles and historical OI; 30-day request window | Expired-token/history depth must be tested. |
| DhanHQ | Expired-options/rolling-option history | Public 2026 issue reports severe 1-minute row truncation; must validate. |
| Shoonya API | Intraday history | API is shallow; archived expired CSV route is preferable. |
| FYERS | Live option chain/WebSocket | Not equivalent to an archived expired-contract history source. |

## Tier C — institutional/exchange-grade
| Source | Capability | Status |
|---|---|---|
| NSE paid real-time/snapshot | NSE 1-minute and 5-minute F&O snapshots; 15-minute delayed 1-minute feed | Authoritative route; historical archive/licensing to establish. |
| TrueData | Historical/real-time option feeds and expired-option data | Strong institutional validation candidate. |
| Global Datafeeds (GDFL) | Market-data WebSocket/API and history functions | Strong institutional validation candidate. |

## Tier D — GitHub/open-source
- i9-tradebot/NIFTY_Options_Historical_Data_Collector: 1-minute NIFTY OHLCV+OI collector using Zerodha.
- mukhilj/breeze_options_pipeline: public 3-year NIFTY 1-minute OHLCV+OI collection pipeline.
- QuantDev-stack/OptionVault: advertises a 300+ GB Indian historical dataset with NIFTY minute/second samples; full dataset is licensed.
- Other GitHub repositories contain collectors/backtesters, but code alone is not evidence of complete historical coverage.

## Source evidence
- OptionsData.shop: https://optionsdata.shop/data/nifty-options-historical-data
- MoneyTicks: https://moneyticks.com/
- Shoonya/Cloud Trader Pro: https://shoonyatrader.in/free-historical-expired-options-contract-data/
- Unfluke: https://unfluke.in/
- Breeze pipeline: https://github.com/mukhilj/breeze_options_pipeline
- Zerodha collector: https://github.com/i9-tradebot/NIFTY_Options_Historical_Data_Collector
- Hugging Face TradeMarkk dataset: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
- Hugging Face Rissin dataset: https://huggingface.co/datasets/rissin/nse-options-intraday
- NSE real-time data: https://www.nseindia.com/static/market-data/real-time-data-subscription
- Unfluke: citeturn2search0
- Breeze pipeline: citeturn1search4
- Shoonya/Cloud Trader Pro: citeturn2search1turn2search11
- MoneyTicks: citeturn2search5turn2search4
- Zerodha: citeturn0search4turn1search2
- Upstox: citeturn0search5
- Angel One: citeturn1search0
- DhanHQ issue: citeturn2search3
- NSE: citeturn0search9
- TrueData/GDFL: citeturn2search7turn1search8
- GitHub collectors/OptionVault: citeturn0search3turn0search7
- Community archive advertisement: citeturn2reddit21turn2reddit24

## Acceptance protocol
Before any source becomes primary research data, obtain a sample containing a D3 date, exact 10:00 IST observation, required CE/PE strikes, timestamp semantics, volume/OI, expired contracts, and weekly-expiry transitions. Audit duplicates/missing minutes and cross-check identical contract/timestamp prices against an independent source.

The Phase 11 hypothesis requires point-in-time 10:00 premiums. EOD bhavcopy data cannot substitute for this intraday requirement.
