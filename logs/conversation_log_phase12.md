# Conversation / Decision Summary — Phase 12

## 2026-10-02 — User scope clarification

User stated that the research should not be limited to OTM6/OTM7/OTM8 and requested examination of **all strikes, open interests, and related variables**.

Decision:
- Start a separate Phase 12 branch.
- Use the complete available NIFTY option surface at 4-DTE/10:00 IST.
- Include premium, OI and volume information.
- Search full-chain structural features rather than only selected OTM premiums.
- Preserve the chronological 2026 holdout and multiple-testing controls.
- Do not authorize trading from a screening result.

Only user-visible requirements and decision summaries are stored; hidden chain-of-thought is not stored.

## 2026-10-02 — Corrected run in progress
User said “Ok proceed”. GitHub Actions run 37009066361 completed acquisition and full-chain extraction successfully and is currently in model analysis. No empirical result is accepted until the run completes and generated outputs are inspected. The live log shows sklearn deprecation/inconsistency warnings but no new fatal exception.

## 2026-10-02 — Timeout and computational correction
The Phase 12 run timed out at 60 minutes during the 500-permutation multiple-testing stage. The scientific protocol is unchanged. The implementation was optimized by caching fold-specific preprocessing and parallelizing the independent label-permutation jobs; the workflow timeout was extended to 120 minutes. No result from the timed-out run is accepted.
