"""The ad-serving allow/deny check: Redis first, Postgres fallback."""
from fastapi import APIRouter, HTTPException

from backend.api.cache.redis_client import read_decision
from backend.api.storage import postgres
from backend.api.storage.moderation_repository import get_ad_decision

router = APIRouter(prefix="/serving", tags=["serving"])


@router.get("/{ad_id}/allowed")
def is_allowed(ad_id: int):
    cached = read_decision(ad_id)
    if cached is not None:
        return {"ad_id": ad_id, "allowed": cached["decision"] == "APPROVED",
                "source": "cache"}

    # Cache miss: fall back to Postgres (and tolerate cold caches).
    conn = postgres.connect()
    try:
        row = get_ad_decision(conn, ad_id)
    finally:
        conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="ad not found")
    if row["status"] == "PENDING":
        raise HTTPException(status_code=409, detail="ad not yet moderated")
    return {"ad_id": ad_id, "allowed": row["status"] == "APPROVED",
            "source": "postgres"}
