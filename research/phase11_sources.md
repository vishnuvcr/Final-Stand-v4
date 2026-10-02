# Phase 11 Sources

## Primary
- Existing Phase 9 cached NIFTY 1-minute data and option data.
- Existing Phase 9 transaction-cost and execution model.
- Phase 9 trade-date split and methodology.

## Derived research inputs
- Entry-day NIFTY spot at 10:00 IST.
- Pre-entry ATR computed solely from prior available NIFTY observations.
- Completed 1-minute NIFTY bars for barrier detection.

## Source-control rule
No new external market-data source is required unless the cached Phase 9 NIFTY series is insufficient. Any new source must be independently validated and recorded before use.
