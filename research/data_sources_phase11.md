# Phase 11 Data Source Assessment

## Candidate A — Hugging Face: rissin/nse-options-intraday

The dataset card reports:
- NIFTY 1-minute intraday option candles from October 2024 through 2026.
- NIFTY daily history from 2001 onward.
- 259 million rows / about 2.51 GB total across the full dataset.
- Fields include timestamp, expiry, strike, option type, OHLC, volume, OI, settlement price, source and granularity.
- The intraday source is attributed to the Upstox historical API; bid/ask is not supplied.
- The dataset license field is shown as "other"; redistribution/use terms must therefore be reviewed before copying large raw files into this repository.

This is currently the leading candidate for the initial reproducible 10:00 IST sample. The research engine should download only the required NIFTY yearly partitions and cache them rather than snapshot the entire 2.5 GB dataset.

Source: https://huggingface.co/datasets/rissin/nse-options-intraday

## Candidate B — SauMStats/nifty-options-data-engine

This public GitHub project documents:
- a 2024 Kaggle historical NIFTY option dataset with 1-minute data,
- NIFTY spot files,
- queries by expiry/trade date/strike/time,
- a 10:00 snapshot interface,
- no bid/ask quotes; market_price is the one-minute close,
- a minimum-volume filter used for liquidity work.

This provides an independent way to reproduce/validate the 2024 slice and the strike/spot join logic.

Source: https://github.com/SauMStats/nifty-options-data-engine

## Candidate C — SatvikBajpai/nifty-options-greeks

This public GitHub project documents six years of NIFTY option history derived from free NSE F&O bhavcopy files, with code to normalize legacy and UDiFF schemas and compute forward/IV/Greeks. The data are primarily daily rather than 10:00 intraday, so it is best used for contract/schema validation and auxiliary daily controls, not as the primary 10:00 predictor input.

Source: https://github.com/SatvikBajpai/nifty-options-greeks

## Candidate D — NSE official option-chain / contract sources

NSE remains the primary reference for:
- NIFTY option contract specifications,
- expiry calendar,
- strike-price interval scheme,
- exchange holidays and contract metadata.

Historical point-in-time intraday chain reconstruction from NSE's current public option-chain page is not assumed to be sufficient by itself; the study must retain provenance for whatever archived intraday source is used.

## Candidate E — Paid full-chain archive

A commercial NIFTY 1-minute full-chain archive was identified with broad historical coverage and OI. It is not treated as the primary source unless a license/purchase is available. It is useful as an independent validation target if obtained lawfully.

## Source policy

The Phase 11 engine will:
1. prefer official NSE metadata and calendars;
2. use a freely accessible intraday dataset for the initial sample;
3. cross-check selected events against an independent source;
4. record source, file, version/hash where available;
5. avoid silently mixing price fields from different sources;
6. preserve licensing/provenance notes.
