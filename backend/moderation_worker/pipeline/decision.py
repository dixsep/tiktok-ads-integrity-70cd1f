"""Fuse rule and ML scores into one decision with explicit thresholds."""
from dataclasses import dataclass

BLOCK_THRESHOLD = 0.85
REVIEW_THRESHOLD = 0.60


@dataclass
class Decision:
    risk_score: float
    decision: str
    reasons: list[str]


def decide(rule_score: float, ml_score: float, reasons: list[str]) -> Decision:
    # Take the more cautious of the two signals.
    risk = max(rule_score, ml_score)
    if risk >= BLOCK_THRESHOLD:
        decision = "BLOCKED"
    elif risk >= REVIEW_THRESHOLD:
        decision = "REVIEW"
    else:
        decision = "APPROVED"
    if not reasons and decision != "APPROVED":
        reasons = [f"model risk score {ml_score:.2f}"]
    return Decision(risk_score=risk, decision=decision, reasons=reasons)
