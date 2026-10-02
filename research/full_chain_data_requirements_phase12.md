# Phase 12 Full-Chain Data Requirements

## Required point-in-time fields

For each target weekly expiry at 10:00:00 IST:
- expiry
- strike
- option_type
- open/high/low/close
- volume
- open_interest
- timestamp
- underlying NIFTY spot

## Preferred additional fields
- bid/ask and quantities
- IV
- change in OI
- futures price/OI
- India VIX
- global-market reference variables

## Source priority

1. NSE official data where legally and technically available.
2. TradeMarkk 1-minute full-chain archive as current reproducible primary.
3. Rissin/Upstox archive for independent price cross-check.
4. Other full-chain sources such as OptionsData.shop or Shoonya only after sample/provenance/licensing validation.

TradeMarkk documents NIFTY option files by expiry and includes strike, option type, volume and open_interest at 1-minute resolution, while warning that illiquid/far strikes may be sparse.

The current Rissin/Upstox intraday archive documents OHLCV and an OI field, but its documentation states OI is NaN for Upstox intraday rows. Therefore it is useful for price replication but is not automatically an independent OI source.

## Acceptance checks

- exact 10:00 timestamp;
- no duplicate strike/type rows;
- no duplicate timestamp rows;
- CE/PE coverage;
- strike-grid continuity;
- nonnegative OI/volume where populated;
- no impossible negative premiums;
- explicit missingness;
- no forward filling across strikes;
- event-level counts of available strikes;
- source provenance.

## Data retention

Commit compact derived event-level feature tables and manifests. Keep large raw archives in the workflow cache/artifact mechanism rather than duplicating large vendor archives into Git.
