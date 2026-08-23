"""Run every policy rule and aggregate the hits."""
from dataclasses import dataclass, field

from backend.moderation_worker.pipeline.rules.policies import ALL_RULES, RuleHit


@dataclass
class RuleResult:
    hits: list[RuleHit] = field(default_factory=list)

    @property
    def rule_ids(self) -> list[str]:
        return [h.rule_id for h in self.hits]

    @property
    def reasons(self) -> list[str]:
        return [h.reason for h in self.hits]

    @property
    def score(self) -> float:
        # Combine deltas without exceeding 1.0 (probabilistic OR).
        product_miss = 1.0
        for h in self.hits:
            product_miss *= (1.0 - h.score_delta)
        return 1.0 - product_miss


def evaluate_rules(features: dict) -> RuleResult:
    hits = [hit for rule in ALL_RULES if (hit := rule(features)) is not None]
    return RuleResult(hits=hits)
