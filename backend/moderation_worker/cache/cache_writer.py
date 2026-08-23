"""Write the latest decision to Redis for the serving gate."""
import json

from backend.moderation_worker.cache.redis_client import get_client

# Long TTL: entries refresh on every decision, the TTL only bounds growth.
DECISION_TTL_SECONDS = 7 * 24 * 60 * 60  # 7 days


def cache_key(ad_id: int) -> str:
    return f"ad:decision:{ad_id}"


def write_decision(ad_id: int, decision: str, risk_score: float,
                   updated_at: str) -> None:
    payload = json.dumps({
        "decision": decision,
        "risk_score": risk_score,
        "updated_at": updated_at,
    })
    get_client().set(cache_key(ad_id), payload, ex=DECISION_TTL_SECONDS)
