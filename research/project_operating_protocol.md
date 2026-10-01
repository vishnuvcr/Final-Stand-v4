# Final Stand v4 — Project Operating Protocol

## Purpose
This repository is the source of truth for the Final Stand research program. Each strategy or material rule change is isolated in a new phase branch and documented before results are accepted.

## Research workflow
1. Check the master research plan, current status, error log, decision log and README before starting a new step.
2. Freeze the strategy specification before empirical testing.
3. Define research questions, aim, objectives, data sources, scientific methodology and statistical analyses.
4. Use public market sources broadly where relevant, including exchange data, open datasets and structured repositories. Prefer cached repository data once validated.
5. Keep each material research phase in a separate Git branch.
6. Each phase workflow must support manual execution with `workflow_dispatch`.
7. Cache important market data and dependency artifacts so repeated runs do not need unnecessary downloads.
8. Log every material failure and corrective action in `logs/error_log.md`.
9. Log strategy interpretation decisions and user-requested changes in `logs/decision_log.md`.
10. Update phase status after every material step and keep README links current.
11. Do not overwrite frozen prior-phase results.
12. Include brokerage, slippage, exchange/statutory charges and other execution costs in trading research.
13. Stop a phase at its documented stopping rule. New strategy variants require a new phase/branch.

## Trading-research defaults
When applicable, evaluate:
- global market crossing inefficiencies,
- NSE/BSE structure,
- option-chain and volatility information,
- FII/DII flows,
- market regime/sentiment,
- major benchmark and volatility indices,
- corporate actions,
- relevant news and event effects,
- liquidity and transaction-cost effects.

These are research dimensions, not mandatory features of every strategy if they are not relevant to the specific hypothesis.

## Reproducibility
Every completed phase should retain:
- strategy specification,
- code and unit tests,
- data-source record,
- workflow definition,
- trade-level ledger,
- data-quality/skips report,
- aggregate statistics,
- interpretation/discussion,
- strengths and limitations,
- conclusion and future research,
- and a structured manuscript for material completed research.

## Conversation record
The repository may contain a factual conversation/decision log and research status history. Private chain-of-thought is not copied into repository files; the repository records decisions, assumptions, errors, results and reproducibility information instead.

## Completion standard
A phase is considered complete only when:
- the specified code passes its tests,
- the empirical run succeeds,
- outputs are validated,
- errors are logged,
- costs/slippage assumptions are explicit,
- results and limitations are documented,
- and README/status files point to the final artifacts.
