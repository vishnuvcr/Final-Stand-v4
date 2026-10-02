# Decision / Conversation Log — Phase 12

## 2026-10-02 — Scope expansion requested
The user clarified that the search should **not be restricted to OTM6/OTM7/OTM8** and should examine **all strikes, open interest, and related option-chain information**.

Decision: create separate Phase 12 branch phase-12-full-chain-oi-direction. The research question is expanded from a six-premium search to the complete point-in-time NIFTY option surface at 4-DTE/10:00 IST.

## Frozen principles
- Existing 4-DTE and 10:00 IST point-in-time convention remains unchanged.
- 2026 remains a chronological holdout.
- All strikes available for the target expiry are eligible.
- OI, volume and price surfaces are eligible when present.
- Missing far/illiquid strikes are represented as missing, never silently forward-filled.
- Model selection occurs only on the development sample.
- Multiple-testing/permutation controls are mandatory.
- No trading translation until out-of-sample and independent-source robustness criteria are met.

## Research boundary
This phase will stop after the defined full-chain feature/model/replication protocol. It will not become an unrestricted feature-mining exercise.

## 2026-10-02 — Model protocol hardening
Before accepting any empirical Phase 12 result, the analysis includes a shallow depth-2 decision-tree benchmark and a bootstrap 95% CI for the frozen 2026 holdout accuracy.

## 2026-10-02 — Permutation diagnostic tightened
The predefined multiple-testing diagnostic was increased from 250 to 500 development-label permutations. The model families, holdout boundary, feature groups and chronological CV protocol remain unchanged.

## 2026-10-02 — Workflow hardening after observed failure
The user-provided Actions screenshot showed the latest Phase 12 run failing after approximately 2m18s. Because the execution marker did not reach the branch and the connector cannot expose push-triggered run logs, the exact failing step could not be verified.

Decision: remove pre-computation marker commits and replace them with always-uploaded step logs. Keep the scientific protocol unchanged. This is an execution/observability correction, not a research-method change.
