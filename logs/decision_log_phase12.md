# Decision / Conversation Log — Phase 12

## 2026-10-02 — Scope expansion requested

### User request
The user clarified that the search should **not be restricted to OTM6/OTM7/OTM8** and should examine **all strikes, open interest, and related option-chain information**.

### Decision
Create a separate Phase 12 branch:
- `phase-12-full-chain-oi-direction`

The research question is expanded from a six-premium search to the complete point-in-time NIFTY option surface at 4-DTE/10:00 IST.

### Frozen principles
- Existing 4-DTE and 10:00 IST point-in-time convention remains unchanged.
- 2026 remains a chronological holdout.
- All strikes available for the target expiry are eligible.
- OI, volume and price surfaces are eligible when present.
- Missing far/illiquid strikes are represented as missing, never silently forward-filled.
- Model selection occurs only on the development sample.
- Multiple-testing/permutation controls are mandatory.
- No trading translation until out-of-sample and independent-source robustness criteria are met.

### Reason for expansion
The prior six-premium search only tests a very small, pre-selected portion of the option surface. It cannot rule out information in:
- OI walls;
- OI imbalance/PCR;
- volume positioning;
- full-wing premium shape;
- ATM-relative skew/curvature;
- max-OI strike locations;
- broader call/put distributions.

### Source evidence
The current TradeMarkk dataset documents 1-minute NIFTY option-chain OHLCV(+OI) with strike and option type and notes sparse coverage for illiquid/far strikes. citeturn0search4turn0search12

Current public full-chain alternatives include OptionsData.shop, which advertises 1-minute NIFTY data for every strike/expiry with OI, and Shoonya, which advertises all strikes with OHLCV+OI; both require sample/provenance validation before use. citeturn0search0turn0search11

NSE's live option-chain schema includes OI, change in OI, volume, IV, LTP and bid/ask fields, establishing the desired variable classes even though the public page is not itself a historical intraday archive. citeturn0search7

## Research boundary

This phase will stop after the defined full-chain feature/model/replication protocol. It will not become an unrestricted feature-mining exercise.
