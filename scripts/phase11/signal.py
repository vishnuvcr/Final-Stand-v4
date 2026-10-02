from __future__ import annotations

from dataclasses import dataclass
from math import isclose


@dataclass(frozen=True)
class PredictorResult:
    call_score: float
    put_score: float
    spread: float
    prediction: str


def compute_scores(
    ce_otm6: float,
    ce_otm7: float,
    ce_otm8: float,
    pe_otm6: float,
    pe_otm7: float,
    pe_otm8: float,
) -> PredictorResult:
    """Compute the Phase 11 premium predictor exactly as specified."""
    call_score = float(ce_otm7 + ce_otm8 - ce_otm6)
    put_score = float(pe_otm7 + pe_otm8 - pe_otm6)
    spread = float(call_score - put_score)

    if isclose(call_score, put_score, rel_tol=0.0, abs_tol=1e-12):
        prediction = "neutral"
    elif call_score > put_score:
        prediction = "bearish"
    else:
        prediction = "bullish"

    return PredictorResult(
        call_score=call_score,
        put_score=put_score,
        spread=spread,
        prediction=prediction,
    )


def realized_direction(spot: float, expiry_settlement: float) -> str:
    """Classify the realized NIFTY move from observation spot to expiry."""
    spot = float(spot)
    expiry_settlement = float(expiry_settlement)
    if isclose(spot, expiry_settlement, rel_tol=0.0, abs_tol=1e-12):
        return "neutral"
    return "bullish" if expiry_settlement > spot else "bearish"


def expiry_return(spot: float, expiry_settlement: float) -> float:
    """Return from observation spot to expiry settlement."""
    if float(spot) == 0.0:
        raise ValueError("spot must be non-zero")
    return float(expiry_settlement) / float(spot) - 1.0
