# Research Status

## Phase 0 — Strategy specification
**Status: COMPLETED**

## Phase 1–5 — V2 baseline
**Status: COMPLETED / FROZEN**

## Phase 6 — Strategy V3 static OTM8 reversal
**Status: COMPLETED / FROZEN**

## Phase 7 — Strategy V4 double-sided OTM16/17
**Status: COMPLETED / FROZEN**

## Phase 8 — Option-data source recovery
**Status: COMPLETED AS A SEPARATE RECOVERY TRACK; source limitations retained**

## Phase 9 — Credit-Selected OTM6/7/8
**Status: COMPLETED — reproducible archive persisted and verified on 2026-10-02**

### Frozen methodology
- Entry: fourth prior trading session before the historical nearest listed expiry, 10:00 IST.
- ATM: nearest 50-point strike, midpoint ties upward.
- Put structure: +1 PE OTM6, -1 PE OTM7, -1 PE OTM8.
- Call structure: +1 CE OTM6, -1 CE OTM7, -1 CE OTM8.
- Compare PE7 + PE8 - PE6 against CE7 + CE8 - CE6; select the higher positive credit; exact positive tie resolves to PUT.
- Target: 90% of initial net-credit flatline after entry slippage.
- Trigger: completed one-minute close; execution at the first common executable next-minute option-bar open.
- Fallback: 15:29 IST expiry open.
- Stop candidates: 0x, 0.50x, 0.75x, 1.00x, 1.25x, 1.50x initial credit.
- Stop selection: chronological development/validation/test split; selection from validation only, using mean net P&L with median and max-drawdown tie-breaks.
- Slippage: 0.10 premium points per option execution.
- Brokerage: ₹10 per unique F&O order.
- Exchange/SEBI/STT/stamp/GST charges use the date-aware implementation.
- Lot size: 75 through 30-Dec-2025 expiry; 65 thereafter.
- No dynamic OTM8 re-centering, reversal, roll, or missing-leg imputation.

### Reproducible execution
- GitHub Actions run: 36970175719 — SUCCESS.
- Unit tests: PASSED (4 tests).
- Computation: 56 executable trades; 26 skipped candidates.
- Output commit: d03d7a1.
- Output commit successfully pushed after fetch/rebase.
- Result files are present on branch phase-9-credit-selected-otm6-8 and their blob SHAs were re-read after the successful push.

### Primary untouched-test result
- Test trades: 12.
- Mean net P&L: ₹1,626.73/trade.
- Median net P&L: ₹2,646.34.
- Total net P&L: ₹19,520.73.
- Win rate: 91.67%.
- Profit factor: 2.22.
- Target hit: 91.67%.
- Stop hit: 0%.
- Expiry fallback: 8.33%.
- Selection: 75% puts / 25% calls.
- Bootstrap 95% CI for test mean: ₹-1,946 to ₹3,869; the interval includes zero.

### Stop sensitivity
On the full 56-trade sample, the no-stop baseline produced mean net P&L ₹2,087.33 and total ₹116,890.46. Positive mean results also occurred at 1.25x and 1.50x stops, but the stop was not selected from the full sample; the frozen validation procedure selected 0x/no stop. This distinction is retained to avoid holdout leakage.

### Target sensitivity
Across the full 56-trade sample:
- 85% target: mean ₹1,991.83.
- 90% target: mean ₹2,087.33.
- 95% target: mean ₹2,099.92.
- 100% target: mean ₹2,186.93.
These are sensitivity observations, not a post-hoc replacement of the frozen 90% primary target.

### Data-quality limitation
The validated option source does not cover every candidate expiry in the calendar window. The 26 skipped candidates are recorded rather than imputed. The result therefore describes the executable historical sample available from the validated source, not every theoretical expiry.

### Scientific interpretation
The untouched test is positive in realized net P&L, but its sample size is only 12 trades and its bootstrap confidence interval includes zero. Therefore the Phase 9 evidence is not sufficient to establish a stable out-of-sample trading edge. Robustness work is required before any stronger inference.

### Phase 10 status
**READY TO START — pre-specified robustness, cost stress, temporal stability, and regime/context analysis.**

Phase 10 must remain on a separate branch and must not modify Phase 9 frozen outputs.