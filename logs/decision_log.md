# Decision / Conversation Log

## 2026-10-01 — Strategy V2 request
User changed the adjustment rule:
1. Initial put: long OTM6 PE, short OTM7 PE, short OTM8 PE.
2. Initial call: long OTM6 CE, short OTM7 CE, short OTM8 CE.
3. Entry: 4 DTE at 10:00 AM.
4. Exit: when P&L reaches approximately the payoff-chart flatline; otherwise expiry/0 DTE.
5. When NIFTY crosses the current OTM8 before expiry, buy back that short OTM8 and sell a newly calculated OTM8 based on the current spot. Repeat whenever the current OTM8 is crossed.

The screenshot example was used to map the initial strikes at spot 23,205.20 with 50-point strikes.

Note: hidden chain-of-thought is not recorded. This log records requirements and implementation decisions only.
