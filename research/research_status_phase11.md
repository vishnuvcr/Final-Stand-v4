# Phase 11 Research Status

**Branch:** phase-11-premium-direction-predictor  
**Status:** Phase 1 — data acquisition BLOCKED by execution environment; no empirical result claimed.  
**Last updated:** 2026-10-02

## Phase status

| Phase | Status |
|---|---|
| 0 — Protocol freeze | IN PROGRESS |
| 1 — Data acquisition/validation | ACQUISITION CODE READY; DATA NOT YET EXECUTED |
| 2 — Feature engineering | CORE SIGNAL + EVENT BUILDER IMPLEMENTED; NOT YET EXECUTED |
| 3 — Primary directional test | NOT STARTED |
| 4 — Out-of-sample validation | NOT STARTED |
| 5 — Robustness/falsification | NOT STARTED |
| 6 — Trading translation | NOT STARTED |
| 7 — Manuscript/conclusion | NOT STARTED |

## Completed in this branch

- Created a separate Phase 11 branch.
- Recorded the exact user-specified premium formulas and directional mapping.
- Completed an initial literature/source review.
- Identified candidate intraday option and NIFTY spot sources.
- Added cached data-acquisition code for NIFTY option Parquet files and NIFTY 1-minute spot CSV files.
- Added the core predictor implementation with unit tests.
- Added an event builder that constructs the 4-DTE/10:00 event table from cached data.
- Added a manual GitHub Actions workflow with validate/acquire/build actions.
- Adopted a point-in-time 10:00 bar-open convention for the primary predictor.

## Latest execution checkpoint — 2026-10-02

- The primary public intraday candidate was independently verified: NIFTY 1-minute option data begins in October 2024 and is partitioned by year. citeturn2search0turn2search3
- Direct acquisition from this chat runtime failed because external DNS/network access to Hugging Face is unavailable.
- The GitHub connector can inspect Actions runs but does not expose the workflow-dispatch write endpoint; the new Phase 11 workflow therefore could not be programmatically started from this chat.
- Existing project/library NIFTY option artifacts were inspected. They are primarily EOD/contract-wise and therefore are not substituted for the required point-in-time 10:00 intraday observations.
- No performance result has been generated or inferred.

## Latest validation note

- Core signal tests and event-builder helper tests are committed. Direct local execution is unavailable in the current container because raw GitHub DNS resolution failed; GitHub Actions remains the execution environment for these tests.

## Data coverage state

No historical event dataset has yet been executed or validated in this branch. Therefore there is **no performance result yet**.

## Current blockers

1. Run the manual acquisition workflow with the required historical years.
2. Validate downloaded option/spot coverage and source schema.
3. Build the event dataset and independently verify a sample of events.
4. Only then run the statistical predictor tests.

## Research-completion rule

The study stops after the defined Phase 7 package. Conclusions will distinguish statistical evidence, economic magnitude, and data-quality uncertainty.


## 2026-10-02 — Expanded source search

A broad public-web search identified multiple independent 1-minute NIFTY option sources. Strong candidates now include OptionsData.shop, Unfluke, ICICI Direct Breeze pipelines, Shoonya/Cloud Trader Pro, MoneyTicks, and community archives; institutional candidates include NSE snapshot feeds, TrueData and Global Datafeeds. Broker APIs including Zerodha, Upstox, Angel One and DhanHQ were also catalogued with their expired-contract limitations. Full inventory: research/phase11/source_inventory.md.

Next gate: acquire and sample-audit at least two independent sources before selecting the Phase 11 primary dataset. Required checks are exact 10:00 IST coverage, expired contracts, CE/PE strikes, timestamp semantics, duplicates/missing bars, and cross-source price agreement.
