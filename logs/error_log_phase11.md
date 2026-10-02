# Error Log — Phase 11

## 2026-10-02

- No research-code error yet.
- Initial branch created from main after checking the existing README, research status, strategy specification, decision log, error log, and available workflows.
- A potential interpretation risk was identified around the meaning of “4 trading days to expiry”; the branch specification freezes this as the trading session four sessions before the actual weekly expiry, with observation at 10:00 IST, consistent with the project's established convention.
- A second interpretation risk was identified around directional labelling: the user's stated mapping is counterintuitive relative to a simple call-vs-put intuition, so the primary hypothesis preserves it exactly and the inverse is reserved for a diagnostic only.
