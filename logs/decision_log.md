# Decision / Conversation Log

## 2026-10-01 — Strategy V2 request
User changed the adjustment rule:
1. Initial put: long OTM6 PE, short OTM7 PE, short OTM8 PE.
2. Initial call: long OTM6 CE, short OTM7 CE, short OTM8 CE.
3. Entry: 4 DTE at 10:00 AM.
4. Exit: when P&L reaches approximately the payoff-chart flatline; otherwise expiry/0 DTE.
5. When NIFTY crosses the current OTM8 before expiry, buy back that short OTM8 and sell a newly calculated OTM8 based on the current spot. Repeat whenever the current OTM8 is crossed.

The screenshot example was used to map the initial strikes at spot 23,205.20 with 50-point strikes.

## 2026-10-02 — Strategy V4 restart
User requested a new four-leg NIFTY structure:
1. Buy 1 OTM16 Call.
2. Sell 2 OTM17 Call.
3. Buy 1 OTM16 Put.
4. Sell 2 OTM17 Put.
5. Enter 4 trading days before expiry at 10:00 AM.

Implementation decision for the omitted exit convention: retain the immediately preceding project's expiry convention — hold to 0 DTE and liquidate at the 15:29 IST option-bar open. No target, roll, reversal or re-centering is applied in V4.

Strike-selection decision: use the 10:00 NIFTY bar open as the entry spot proxy to avoid selecting strikes from the close of the same minute.

Branching decision: V4 is isolated on phase-7-double-sided-otm16-17 and does not overwrite V2/V3 outputs.



## 2026-10-02 — V4 backtest conclusion
The accepted GitHub Actions rerun completed successfully. The final sample contains 43 complete four-leg trades from 92 candidate expiries. Net P&L after modeled costs is INR 84,698.69. All 43 terminal results are positive, but all 43 trades experienced negative intratrade gross MTM; the worst observed gross MTM trough is -INR 24,394.50. The phase is closed with the result interpretation and manuscript committed on the phase-7 branch. Further parameter/exit exploration requires a new phase.
