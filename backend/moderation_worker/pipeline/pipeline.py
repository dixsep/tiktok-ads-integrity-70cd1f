"""The full pipeline: features -> rules -> ML -> decision."""
from dataclasses import dataclass, field

from backend.moderation_worker.pipeline.features import extract_features
from backend.moderation_worker.pipeline.rules_engine import evaluate_rules
from backend.moderation_worker.pipeline.ml_scorer import ml_risk_score
from backend.moderation_worker.pipeline.decision import decide


@dataclass
class ModerationResult:
    ad_id: int
    risk_score: float = 0.0
    decision: str = "APPROVED"
    rule_hits: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)


def run_pipeline(ad: dict) -> ModerationResult:
    features = extract_features(ad)
    rules = evaluate_rules(features)
    ml_score = ml_risk_score(features, rules.score)
    outcome = decide(rules.score, ml_score, rules.reasons)
    return ModerationResult(
        ad_id=ad["id"],
        risk_score=outcome.risk_score,
        decision=outcome.decision,
        rule_hits=rules.rule_ids,
        reasons=outcome.reasons,
    )
