# Phase 12 Research Status

**Branch:** phase-12-full-chain-oi-direction  
**Status:** Phase 1 implementation complete; empirical full-chain extraction/model run initiated via GitHub Actions.  
**Last updated:** 2026-10-02

## Scope

This phase expands the prior six-premium search to **all available NIFTY strikes at 4-DTE/10:00 IST**, including option premium, open interest and volume surfaces.

## Phase status

| Phase | Status |
|---|---|
| 0 — Scope/protocol expansion | COMPLETE |
| 1 — Full-chain extraction | CODE COMPLETE; CI RUN PENDING |
| 2 — Feature engineering | CODE COMPLETE |
| 3 — Model screening | CODE COMPLETE |
| 4 — Holdout/multiple-testing | CODE COMPLETE |
| 5 — Independent replication/robustness | NOT STARTED |
| 6 — Trading translation | NOT STARTED |
| 7 — Manuscript | NOT STARTED |

## Frozen protocol

- 4 trading sessions before weekly expiry.
- 10:00:00 IST one-minute bar OPEN.
- All available strikes for the target expiry.
- CE/PE premium, OI and volume where present.
- ATM-relative strike-distance representation.
- No forward filling/interpolation across missing strikes.
- Development: expiries before 2026.
- Holdout: expiries in 2026.
- Model selection only on development.
- Multiple-testing permutation diagnostic.
- No trading translation without robust holdout evidence.

## Feature families

1. Full ATM-relative surface vectors from -30 to +30 strike-grid units.
2. Total CE/PE premium, OI and volume.
3. PCR and call/put imbalance.
4. OI/volume/premium-weighted strike location and dispersion.
5. Maximum OI/volume/premium wall location and concentration.
6. Full-chain aggregate and surface models.

## Current data source

The primary acquisition reuses the validated Phase 11 TradeMarkk NIFTY 1-minute option archive. Its dataset documentation states that the option records contain timestamp, OHLCV, open interest, strike and option type and warns that illiquid/far strikes can be sparse.

The extraction produces a compact event-level feature table; raw archives remain in the GitHub Actions cache rather than being copied into Git.

## Next gate

Run the Phase 12 manual workflow. After extraction, inspect:
- number of available strikes per event;
- exact 10:00 coverage;
- OI/volume missingness;
- selected development model;
- 2026 holdout balanced accuracy/MCC;
- permutation p-value.

Then either proceed to independent replication or close the phase as negative/inconclusive. No further unconstrained feature mining is planned.
