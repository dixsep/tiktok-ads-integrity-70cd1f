"""Moderation detail + review-queue listing endpoints."""
from fastapi import APIRouter, HTTPException, Query

from backend.api.storage import postgres
from backend.api.storage.moderation_repository import get_ad_detail, list_by_status

router = APIRouter(prefix="/moderation", tags=["moderation"])

_ALLOWED_STATUSES = {"PENDING", "APPROVED", "BLOCKED", "REVIEW"}


@router.get("/ads/{ad_id}")
def ad_detail(ad_id: int):
    conn = postgres.connect()
    try:
        ad = get_ad_detail(conn, ad_id)
    finally:
        conn.close()
    if ad is None:
        raise HTTPException(status_code=404, detail="ad not found")
    return ad


@router.get("/queue")
def review_queue(
    status: str = Query("REVIEW"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    if status not in _ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail="invalid status filter")
    conn = postgres.connect()
    try:
        items = list_by_status(conn, status, limit, offset)
    finally:
        conn.close()
    return {"status": status, "limit": limit, "offset": offset, "items": items}
