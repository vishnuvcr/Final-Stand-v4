from pathlib import Path
import pandas as pd
import subprocess
import sys

SCRIPT = Path("scripts/phase10_context_join.py")


def test_context_join_script_exists():
    assert SCRIPT.exists()


def test_context_join_uses_lagged_merge():
    text = SCRIPT.read_text()
    assert "allow_exact_matches=False" in text
    assert 'direction="backward"' in text


def test_context_outputs_are_declared_in_workflow():
    wf = Path(".github/workflows/phase-10-v5-robustness-context.yml").read_text()
    assert "python scripts/phase10_context_join.py" in wf


def test_context_output_schema_if_present():
    path = Path("results/phase10_market_context.csv")
    if not path.exists():
        return
    df = pd.read_csv(path)
    required = {"entry_date", "side", "net_pnl"}
    assert required.issubset(df.columns)
    assert len(df) > 0

def test_context_join_handles_unavailable_nse_json_and_nifty_fallback():
    script = Path("scripts/phase10_context_join.py").read_text()
    assert "json.JSONDecodeError" in script
    assert "stooq_nifty.csv" in script

def test_context_acquisition_includes_nifty_fallback():
    script = Path("scripts/phase10_market_context.py").read_text()
    assert '"^nsei", "stooq_nifty.csv"' in script
