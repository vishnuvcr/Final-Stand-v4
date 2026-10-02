import pytest

from scripts.phase11.signal import compute_scores, expiry_return, realized_direction


def test_primary_mapping_call_greater_means_bearish():
    result = compute_scores(
        ce_otm6=10, ce_otm7=8, ce_otm8=7,
        pe_otm6=5, pe_otm7=4, pe_otm8=3,
    )
    assert result.call_score == 5
    assert result.put_score == 2
    assert result.spread == 3
    assert result.prediction == "bearish"


def test_primary_mapping_put_greater_means_bullish():
    result = compute_scores(
        ce_otm6=5, ce_otm7=4, ce_otm8=3,
        pe_otm6=10, pe_otm7=8, pe_otm8=7,
    )
    assert result.call_score == 2
    assert result.put_score == 5
    assert result.spread == -3
    assert result.prediction == "bullish"


def test_tie_is_neutral():
    result = compute_scores(
        ce_otm6=10, ce_otm7=7, ce_otm8=3,
        pe_otm6=10, pe_otm7=7, pe_otm8=3,
    )
    assert result.spread == 0
    assert result.prediction == "neutral"


def test_realized_direction():
    assert realized_direction(100, 105) == "bullish"
    assert realized_direction(100, 95) == "bearish"
    assert realized_direction(100, 100) == "neutral"


def test_expiry_return():
    assert expiry_return(100, 105) == pytest.approx(0.05)


def test_expiry_return_rejects_zero_spot():
    with pytest.raises(ValueError):
        expiry_return(0, 100)
