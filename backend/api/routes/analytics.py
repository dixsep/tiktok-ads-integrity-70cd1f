"""Analytics endpoints backing the dashboard's summary tables."""
from fastapi import APIRouter, Query

from backend.api.storage import postgres
from backend.api.storage.analytics_repository import (
    decision_counts,
    top_rule_hits,
    advertiser_risk,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def summary(days: int = Query(7, ge=1, le=90)):
    conn = postgres.connect()
    try:
        return {
            "window_days": days,
            "decision_counts": decision_counts(conn, days),
            "top_rule_hits": top_rule_hits(conn, limit=10),
            "advertiser_risk": advertiser_risk(conn, limit=10),
        }
    finally:
        conn.close()
