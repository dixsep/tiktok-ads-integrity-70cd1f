"""Each rule is a pure function: features -> RuleHit | None.

A RuleHit carries a stable id (for analytics), a human reason, and a score
contribution in [0, 1]. Rules never raise and never mutate the input.
"""
from dataclasses import dataclass

PROHIBITED_KEYWORDS = {
    "guaranteed returns", "miracle cure", "work from home now",
    "double your money", "free crypto",
}
SUSPICIOUS_TLDS = {".zip", ".top", ".click", ".xyz"}


@dataclass(frozen=True)
class RuleHit:
    rule_id: str
    reason: str
    score_delta: float


def rule_prohibited_keyword(f: dict) -> RuleHit | None:
    for kw in PROHIBITED_KEYWORDS:
        if kw in f["text"]:
            return RuleHit("RULE_PROHIBITED_KEYWORD",
                           f"contains prohibited phrase '{kw}'", 0.6)
    return None


def rule_excessive_punctuation(f: dict) -> RuleHit | None:
    if f["exclaim_runs"] >= 1 or f["upper_ratio"] > 0.6:
        return RuleHit("RULE_EXCESSIVE_PUNCTUATION",
                       "shouty formatting (caps / repeated punctuation)", 0.25)
    return None


def rule_suspicious_domain(f: dict) -> RuleHit | None:
    domain = f["landing_domain"]
    if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS):
        return RuleHit("RULE_SUSPICIOUS_DOMAIN",
                       f"landing domain uses a high-risk TLD ({domain})", 0.4)
    return None


def rule_mismatched_creative_host(f: dict) -> RuleHit | None:
    host, domain = f["creative_host"], f["landing_domain"]
    if host and domain and not host.endswith(domain) and not domain.endswith(host):
        return RuleHit("RULE_MISMATCHED_HOST",
                       f"creative host '{host}' does not match landing '{domain}'", 0.3)
    return None


ALL_RULES = [
    rule_prohibited_keyword,
    rule_excessive_punctuation,
    rule_suspicious_domain,
    rule_mismatched_creative_host,
]
