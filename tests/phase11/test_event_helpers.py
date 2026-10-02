import numpy as np

from scripts.phase11.build_events import infer_step, nearest_strike


def test_infer_step_uses_modal_strike_interval():
    strikes = np.array([22000, 22050, 22100, 22150, 22200], dtype=float)
    assert infer_step(strikes) == 50


def test_nearest_strike_breaks_tie_upward():
    strikes = np.array([22000, 22050], dtype=float)
    assert nearest_strike(strikes, 22025) == 22050
