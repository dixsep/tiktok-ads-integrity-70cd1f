"""API-side cache write, used when a human override changes a decision."""
import json

from backend.api.cache.redis_client import get_client

DECISION_TTL_SECONDS = 7 * 24 * 60 * 60


def write_decision(ad_id: int, decision: str, risk_score: float | None,
                   updated_at: str) -> None:
    payload = json.dumps({
        "decision": decision,
        "risk_score": risk_score,
        "updated_at": updated_at,
    })
    get_client().set(f"ad:decision:{ad_id}", payload, ex=DECISION_TTL_SECONDS)
