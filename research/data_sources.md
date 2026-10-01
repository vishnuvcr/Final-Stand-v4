# Data Sources and Validation Register

1. NSE NIFTY 50 F&O contract specification — primary exchange reference for contract descriptors, expiry rules, strike interval and tick size.
2. NSE historical derivatives reports / contract-wise price-volume archives — exchange reference for EOD validation.
3. Hugging Face rissin/nse-options-intraday — primary intraday option candidate for this phase; Upstox 1-minute option candles, Oct 2024 onward, with expiry/strike/type/OHLC/volume/OI fields.
4. GitHub technovusin/nifty50-historical-data — NIFTY 1-minute spot OHLC candidate.
5. Other public GitHub datasets/pipelines are validation/availability cross-checks only.

## Known data limitation
The primary intraday option source does not provide historical bid/ask. Exact market-depth execution and spread costs cannot be reconstructed. The research must model slippage and clearly distinguish observed prices from modeled execution.
