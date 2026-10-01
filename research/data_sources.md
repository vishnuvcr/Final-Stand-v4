# Data Sources and Validation Register

1. NSE NIFTY 50 F&O contract specification — primary exchange reference for contract descriptors, expiry rules, strike interval and tick size.
2. NSE historical derivatives reports / contract-wise price-volume archives — exchange reference for EOD validation.
3. Hugging Face rissin/nse-options-intraday — primary intraday option candidate for this phase; Upstox 1-minute option candles, Oct 2024 onward, with expiry/strike/type/OHLC/volume/OI fields.
4. GitHub technovusin/nifty50-historical-data — NIFTY 1-minute spot OHLC candidate.
5. Other public GitHub datasets/pipelines are validation/availability cross-checks only.

## Known data limitation
The primary intraday option source does not provide historical bid/ask. Exact market-depth execution and spread costs cannot be reconstructed. The research must model slippage and clearly distinguish observed prices from modeled execution.

## Validation evidence added 2026-10-01
- Hugging Face dataset card documents 259M rows, Parquet format, 1-minute NIFTY coverage from Oct 2024 onward, and the canonical schema including timestamp, expiry, strike, option type and OHLC.
- NSE current contract specification documents Tuesday expiry for NIFTY 50 index options and a 50-point strike interval for weekly/monthly contracts.
- NSE Circular FAOP64625 revised NIFTY lot size from 25 to 75 for new index derivative contracts introduced from 20-Nov-2024.
- NSE Circular FAOP70616 revised NIFTY lot size from 75 to 65 effective after the 30-Dec-2025 expiry; existing weekly/monthly contracts retained 75 through that expiry.
- Paytm Money's current F&O FAQ states ₹10 brokerage per unique executed order. Historical Paytm Money documentation states ₹20 for users opening accounts on/after 25-Aug-2023, while earlier users remained at ₹10. The backtest therefore exposes brokerage as a parameter and will test both ₹10 and ₹20.
