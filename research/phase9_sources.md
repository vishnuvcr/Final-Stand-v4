# Phase 9 Sources and Research Context

## Exchange / contract mechanics
- NSE NIFTY 50 F&O contract specifications: https://www.nseindia.com/static/products-services/equity-derivatives-nifty50
- NSE contract specifications: https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications
- NSE circular on the expiry-day transition: https://nsearchives.nseindia.com/content/circulars/FAOP68589.pdf and https://nsearchives.nseindia.com/content/circulars/FAOP68747.pdf
- NSE levies / STT / stamp / GST reference: https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies
- NSE transaction-charge revision effective 1-Mar-2026: https://nsearchives.nseindia.com/content/circulars/FA73061.pdf

## Broker cost
- Paytm Money F&O FAQ currently states ₹10 brokerage per unique executed F&O order: https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web

## Intraday option data
- Hugging Face dataset: https://huggingface.co/datasets/rissin/nse-options-intraday
- Pinned README revision used in Phase 9: 78b1c54.
- Dataset documentation states the intraday NIFTY track is 1-minute, October 2024 onward, with OHLC, strike, expiry and option type fields.

## Existing repository evidence
- Final Stand v4 Phase 7 already validated the spot-source layout and historical NIFTY lot-size handling used here.
- Phase 8 independently audited additional option-data sources; Phase 9 does not replace the existing accepted data silently.

## Broader research controls
The primary backtest deliberately does not select trades using India VIX, FII/DII, global equity indices, USD/INR, gold, news or corporate-action signals. These variables remain regime-analysis candidates for a later locked phase so that they cannot become post-hoc filters.