# Phase 8 — Option Data Source Recovery Audit

## Purpose
Investigate independent historical NIFTY option-data sources that may recover the 49 candidate expiries skipped in Phase 7 because one or more required 1-minute option observations were unavailable.

## Frozen Phase 7 requirement
The recovery dataset must support, for each candidate expiry where possible:
- NIFTY weekly option contracts
- OTM16 and OTM17 CE and PE
- exact expiry
- 10:00 IST entry-minute OHLC, using the 10:00 bar open
- expiry-day 15:29 IST OHLC, using the 15:29 bar open
- contract-level strike, option type and expiry identifiers
- no imputation of missing prices

## Sources reviewed

### 1. ICICI Direct Breeze API — primary candidate
Official Breeze documentation states that historical charts support NSE/NFO options and 1-minute interval data, with explicit parameters for expiry date, option right and strike price. The API documentation also shows NIFTY NFO option examples and open-interest fields.
Evidence: https://api.icicidirect.com/breezeapi/documents/index.html
Strengths: contract-specific historical option retrieval; 1-minute resolution; explicit expiry/right/strike parameters; suitable for targeted recovery of only the missing contracts.
Constraints: requires an ICICI Direct Breeze API credential/session; API rate limits apply; credentials must remain outside the repository.
Assessment: High-priority recovery source if credentials are available.

### 2. TradeMarkk / india-index-options-1m — strong public cross-check
Hugging Face dataset thetrademarkk/india-index-options-1m reports approximately 2021–2026 1-minute NSE/BSE index and option-chain data. Its schema includes timestamp, OHLCV, open interest, strike, option type and expiry. The dataset explicitly warns that far/illiquid strikes can be sparse or absent.
Evidence: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
Assessment: High-priority public cross-check, but expected to have the same deep-OTM sparsity problem for some contracts.

### 3. TradeMarkk bucket mirror
A Hugging Face bucket contains the same India Index & Options 1-minute dataset family, with thousands of files and approximately 4 GB total storage.
Evidence: https://huggingface.co/buckets/codepyx23/india-index-options-1m-bucket
Assessment: Useful for bulk/cached retrieval if licensing and dataset provenance are acceptable; not automatically independent from the TradeMarkk dataset.

### 4. OptionsData.shop — commercial full-chain candidate
The provider advertises NIFTY 1-minute full-chain historical data covering all strikes and expiries, with open interest, and reports coverage through September 2026.
Evidence: https://optionsdata.shop/data/nifty-options-historical-data
Assessment: Potentially the most direct way to recover deep-OTM gaps, subject to purchase/licensing and independent validation.

### 5. Global Datafeeds — commercial API candidate
Global Datafeeds documents historical NFO futures/options data with tick/minute/day/week/month periodicities and contractwise NFO option symbols.
Evidence: https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/introduction/type-of-data-available/
Assessment: Potential institutional-quality recovery source; access/licensing must be established before implementation.

### 6. Dhan rolling-options API — not selected as primary source
A public DhanHQ GitHub issue documents missing historical rows from its rolling-options endpoint, specifically affecting expired NIFTY options and making the data unsuitable for some backtesting use cases.
Evidence: https://github.com/dhan-oss/DhanHQ-py/issues/153
Assessment: Do not use as the primary recovery source without validating completeness contract-by-contract.

### 7. Zerodha/Kite-derived public collectors
Several public repositories demonstrate 1-minute historical NIFTY option collection through Zerodha APIs, but access requires a valid authenticated account/token and historical retention/API constraints must be verified.
Examples: https://github.com/i9-tradebot/NIFTY_Options_Historical_Data_Collector ; https://github.com/vikassharma545/Historical-Market-data-From-Zerodha
Assessment: Possible secondary authenticated source, not yet validated for complete 2025–2026 deep-OTM coverage.

## Recommended recovery order
1. ICICI Breeze targeted recovery, if a valid credential can be supplied securely.
2. TradeMarkk public dataset as an independent bulk cross-check.
3. Commercial full-chain source (OptionsData.shop or Global Datafeeds) if public/authenticated sources cannot recover the gaps.
4. Zerodha-derived source as another authenticated cross-check.
5. Dhan only after explicit completeness testing.

## Validation rule
A recovered observation may replace a missing Phase 7 observation only if:
- contract identity matches expiry, strike and CE/PE;
- timestamp is exactly the required 10:00 or 15:29 IST minute;
- OHLC fields are present;
- no interpolation or synthetic reconstruction is used;
- source provenance is recorded;
- source conflicts are retained for audit rather than silently overwritten.

## Important methodological rule
Do not merge sources blindly. The same contract should be compared across sources where overlap exists. Differences in timestamps, adjusted prices, contract naming, expired-contract retention, or missing-row policy must be documented before adding recovered trades to the accepted sample.

## Current status
Phase 8A — source discovery: COMPLETE
Phase 8B — source acquisition: NOT STARTED

No Phase 7 result has been changed by this audit.
## Phase 8B source acquisition assessment — 2026-10-02

### Public source result
The public TradeMarkk/Hugging Face route was implemented as an isolated recovery workflow, but the workflow result is not accessible through the connected GitHub Actions interface in this session. No recovered trade is therefore accepted on the basis of an unverified run.

### Strongest complete archive identified
OptionsData.shop currently advertises NIFTY 1-minute full-chain history with every strike and expiry, including expired contracts, through September 2026. Its published archive description states that the data are contract-level OHLC, volume and open interest in Parquet, with NIFTY options covering June 2021 through September 2026. It also states that the archive is derived from the ICICI Breeze API.

Web evidence:
- NIFTY 1-minute full chain: https://optionsdata.shop/data/nifty-options-historical-data
- Expired option contracts: https://optionsdata.shop/data/expired-option-contracts-data
- 2025 pack: https://optionsdata.shop/packs/nifty-options-1-minute-2025
- 2026 last-three-month pack: https://optionsdata.shop/packs/nifty-options-1-minute-last-3-months

### Independent API route
ICICI Direct's official Breeze documentation confirms that historical NFO options can be requested at 1-minute resolution by expiry date, option right and strike price. The documented API limit is 100 calls/minute and 5,000 calls/day.

Web evidence:
- https://api.icicidirect.com/breezeapi/documents/index.html

### Acquisition blocker
No ICICI Breeze credentials or purchased commercial archive are available to this session. Therefore Phase 8 cannot legitimately claim recovery of the 49 skipped trades yet.

### Decision
Do not alter the Phase 7 accepted ledger.
Do not impute missing prices.
Do not claim public-source recovery without a verifiable CI result.
The next executable recovery route is either:
1. provide/use an authorized Breeze API credential through a secure repository secret, or
2. acquire the relevant OptionsData.shop archive and place it in the repository's protected/cached data workflow.

Phase 8 remains open until acquisition and validation are completed.
