from pathlib import Path

def test_phase10_plan_exists():
    assert Path("research/phase10_research_plan.md").exists()

def test_phase10_sources_exists():
    assert Path("research/phase10_sources.md").exists()

def test_phase10_runner_exists():
    assert Path("scripts/phase10_robustness.py").exists()

def test_phase9_engine_exists():
    assert Path("scripts/backtest_v5_credit_selected.py").exists()
