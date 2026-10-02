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

## 2026-10-02 — Execution-marker failure / insufficient observability
The user-provided GitHub Actions screenshot shows the latest Phase 12 workflow run failing after approximately 2m18s. The expected repository execution-start marker was not present, so the exact failing step could not be established from the repository connector.

The execution-marker design has therefore been removed. It was unnecessary for the scientific protocol and introduced an extra in-run git push before computation. The hardened workflow now:
- validates required files before acquisition;
- records stdout/stderr for installation, acquisition, extraction and analysis;
- uploads those diagnostics as an artifact even on failure;
- does not mutate the branch before computation;
- publishes derived research outputs to the branch only after a successful analysis;
- retains the 60-minute execution timeout and concurrency protection.

No empirical Phase 12 result is claimed from the failed run.

## 2026-10-02 — Model-analysis failure diagnosed from Actions logs
The first full-chain computation successfully completed acquisition and feature extraction but failed during model screening because some feature columns were entirely missing within a chronological training fold. Median imputation returned NaN for those columns, and scikit-learn LogisticRegression rejected the resulting matrix.

This was a genuine analysis-code defect, not a data/result finding. The correction drops only features with no finite training observations within each fold, then median-imputes remaining missing values using the training fold. The same training-derived feature filtering is applied to holdout fitting and the tree benchmark. No outcomes or holdout observations are used to decide feature availability.

The workflow log showed the failure at scripts/phase12/analyze_full_chain.py with ValueError: Input X contains NaN. No empirical Phase 12 result from that run is accepted.

## 2026-10-02 — Corrected run monitoring
The corrected run 37009066361 entered model analysis successfully after the all-missing-feature fix. Current logs show sklearn deprecation/inconsistency warnings only; no new fatal error has been observed. This remains an execution status, not a research result.
