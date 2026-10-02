# Error Log — Phase 12

## 2026-10-02 — Scope expansion

No research-code error. Phase 12 was created because the prior Phase 11 six-premium search cannot answer whether information exists elsewhere on the full option chain.

## 2026-10-02 — Data-source constraint

The Rissin/Upstox secondary archive documents an OI field but states that OI is NaN for Upstox intraday rows. It will therefore be used primarily for price replication, not assumed as an independent OI source.

## 2026-10-02 — Complexity control

The full-chain phase deliberately limits model families and uses regularized logistic regression plus chronological cross-validation. This is necessary because the event sample is only 121 observations while the full-chain surface contains many potential variables.

No empirical result has been generated yet.

## 2026-10-02 — CI trigger correction
The initial Phase 12 status-file commit did not match the workflow push-path filter, so it did not itself trigger Actions. The workflow was corrected to include the Phase 12 status/error files and to upload derived results as an artifact. A subsequent workflow-file commit now provides the push trigger.

## 2026-10-02 — Duplicate-run cascade observed
The Actions screen showed multiple Phase 12 runs queued/in progress from successive documentation commits. This was caused by including status/log documentation paths in the push trigger. The workflow was narrowed to workflow/code changes and a concurrency group with cancel-in-progress was added. Manual dispatch remains available.
