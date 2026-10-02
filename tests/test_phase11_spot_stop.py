from pathlib import Path
import ast

def test_script_parses():
    ast.parse(Path("scripts/phase11_spot_stop.py").read_text())

def test_candidate_grid_is_frozen():
    s=Path("scripts/phase11_spot_stop.py").read_text()
    for x in ["50,75,100,125,150,200","0.0025,0.0040,0.0050,0.0075,0.0100","0.50,0.75,1.00,1.25,1.50"]:
        assert x in s

def test_adverse_direction_matches_payoff():
    s=Path("scripts/phase11_spot_stop.py").read_text()
    assert "entry_spot - SPOT_STOP_VALUE if side=='PUT' else entry_spot + SPOT_STOP_VALUE" in s
    assert "entry_spot*(1.0-SPOT_STOP_VALUE) if side=='PUT' else entry_spot*(1.0+SPOT_STOP_VALUE)" in s
    assert "entry_spot - SPOT_STOP_VALUE*atr_value if side=='PUT' else entry_spot + SPOT_STOP_VALUE*atr_value" in s
    assert "float(bar['low']) <= spot_barrier" in s
    assert "float(bar['high']) >= spot_barrier" in s

def test_phase11_plan_freezes_holdout():
    s=Path("research/phase11_research_plan.md").read_text()
    assert "untouched test" in s.lower()
    assert "validation" in s.lower()
