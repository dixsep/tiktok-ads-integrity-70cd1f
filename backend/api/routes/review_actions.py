"""Moderator override endpoints, gated by a static API key."""
import os
from datetime import datetime, timezone

from fastapi import APIRouter, Header, HTTPException

from backend.api.storage import postgres
from backend.api.storage.review_repository import apply_override
from backend.api.cache.cache_writer import write_decision
from backend.api.events.kafka_producer import publish_override

router = APIRouter(prefix="/review", tags=["review"])

_MODERATOR_KEY = os.environ.get("MODERATOR_API_KEY", "dev-moderator-key")


def _require_moderator(x_moderator_key: str | None) -> str:
    if x_moderator_key != _MODERATOR_KEY:
        raise HTTPException(status_code=401, detail="moderator key required")
    return "moderator"  # a real system resolves this to an identity


def _act(ad_id: int, decision: str, moderator: str):
    conn = postgres.connect()
    try:
        applied = apply_override(conn, ad_id, decision, moderator)
    finally:
        conn.close()
    if not applied:
        raise HTTPException(status_code=409, detail="ad is not in REVIEW")
    write_decision(ad_id, decision, None,
                   datetime.now(timezone.utc).isoformat())
    publish_override(ad_id, decision, moderator)
    return {"ad_id": ad_id, "decision": decision}


@router.post("/ads/{ad_id}/approve")
def approve(ad_id: int, x_moderator_key: str | None = Header(default=None)):
    moderator = _require_moderator(x_moderator_key)
    return _act(ad_id, "APPROVED", moderator)


@router.post("/ads/{ad_id}/block")
def block(ad_id: int, x_moderator_key: str | None = Header(default=None)):
    moderator = _require_moderator(x_moderator_key)
    return _act(ad_id, "BLOCKED", moderator)
