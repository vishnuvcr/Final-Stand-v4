# Error Log — Phase 11

## 2026-10-02

- No research-code error yet.
- Initial branch created from main after checking the existing README, research status, strategy specification, decision log, error log, and available workflows.
- A potential interpretation risk was identified around the meaning of “4 trading days to expiry”; the branch specification freezes this as the trading session four sessions before the actual weekly expiry, with observation at 10:00 IST, consistent with the project's established convention.
- A second interpretation risk was identified around directional labelling: the user's stated mapping is counterintuitive relative to a simple call-vs-put intuition, so the primary hypothesis preserves it exactly and the inverse is reserved for a diagnostic only.


## 2026-10-02 — Initial GitHub Actions validation

- The first Phase 11 workflow run (run 1) completed with a failure immediately after the workflow file was added; the connector exposed no jobs for the run, so the exact runner-step failure was not available.
- The workflow file itself was fetched back from the branch and reviewed; it was simplified to a manual-run-only validation workflow to reduce self-triggering and write-permission failure modes.
- No market-data analysis was performed under the failed run, so no research result is affected.


## 2026-10-02 — Local runtime validation limitation

- An attempt to run the new Phase 11 Python tests directly in the model container could not download the branch files because DNS resolution for raw.githubusercontent.com is unavailable in that container.
- This is an environment/network limitation, not a detected research-code failure.
- The same tests are wired into the Phase 11 GitHub Actions workflow, where validation is intended to run.
- No market-data result was generated or inferred from the failed local execution.


## 2026-10-02 — Tooling/editing mistake

- One early attempt to write the acquisition/build code failed due to an unescaped template/interpolation token in the orchestration script; no repository file was corrupted by that attempt.
- The write was corrected and the intended files were committed successfully.


## 2026-10-02 — Phase 1 acquisition blocker

- Direct Hugging Face access from the execution container failed with DNS resolution error for huggingface.co.
- GitHub Actions workflow dispatch is not available through the connected GitHub action surface, so the Phase 11 acquisition workflow could not be manually launched from this chat.
- A push-triggered version of the Phase 11 workflow was committed, but no corresponding Phase 11 run appeared in the accessible workflow-run list at the checkpoint.
- Existing project-library NIFTY option artifacts were considered and rejected as substitutes because they are EOD/contract-wise rather than the required 10:00 intraday option observations.
- This is a data-access/execution blocker, not a statistical result. The study remains open at Phase 1.


## 2026-10-02 — CI failure diagnosed and corrected

- Workflow run for commit `542b972ce226cf0d5a0b9773b3ed414215112883` was accessed directly through the GitHub Actions check-run/job logs.
- Run completed in ~17 seconds and failed during **pytest collection**, before any market-data acquisition.
- Exact error: both `tests/phase11/test_event_helpers.py` and `tests/phase11/test_signal.py` raised `ModuleNotFoundError: No module named 'scripts'`.
- Root cause: the repository did not explicitly package the `scripts` and `scripts/phase11` directories, and the CI test invocation did not force the repository root onto `PYTHONPATH`.
- Correction: added `scripts/__init__.py`, `scripts/phase11/__init__.py`, and set `PYTHONPATH: ${{ github.workspace }}` at the Phase 11 job level.
- No market-data result was produced by the failed run, so the research conclusions remain unaffected.


## 2026-10-02 — CI cache-key failure diagnosed and corrected

- The next run after the Python import fix reached all 8 unit tests successfully: **8 passed**.
- It then failed in `actions/cache@v4` before acquisition.
- Exact error: `Key Validation Error ... cannot contain commas`.
- Cause: the cache key incorporated the workflow input `2024,2025,2026` literally.
- Correction: removed the year-list suffix from the cache key and retained the research data-manifest hash as the cache identity.
- This failure occurred before market-data acquisition; no empirical result was generated.


## 2026-10-02 — Cross-source audit memory failure diagnosed

- Two consecutive Phase 11 runs successfully completed acquisition and event construction (132 expiry candidates; 121 events).
- Both runs then terminated during `cross_source_audit.py` while loading the secondary archive, with GitHub reporting a runner shutdown signal and operation cancellation.
- The audit implementation loaded all 2024–2026 secondary option rows simultaneously. This created unnecessary memory pressure because the primary archive had already been loaded by the event builder.
- Correction: the audit now processes one secondary year file at a time and reads only the five required columns.
- Push-triggered runs now reuse the committed event dataset when it already exists; full event reconstruction remains available through manual `build`.
- No statistical result was invalidated. The already-completed statistical analysis remains reproducible from the committed event dataset.


## 2026-10-02 — Premium-search result persistence / CI push race

- The premium-combination analysis itself completed successfully: acquisition, independent source audit, statistical analysis, and premium search all passed.
- The final CI commit step created the derived files in the runner but the subsequent git push failed with a non-fast-forward rejection because the branch had advanced concurrently.
- This did not invalidate the analysis. The derived JSON/Markdown results were reconstructed from the completed Actions log and persisted directly to the branch through the GitHub file API.
- Future workflow commit logic should rebase/pull or use a serialized write path before pushing derived results, to avoid concurrent-branch races.
