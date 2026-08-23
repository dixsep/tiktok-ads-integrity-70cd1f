"""Ad submission route: validate -> persist (PENDING) -> emit event."""
from fastapi import APIRouter, HTTPException

from backend.api.models import AdSubmission, AdCreated
from backend.api.storage import postgres
from backend.api.events.kafka_producer import publish_ad_submitted

router = APIRouter(prefix="/ads", tags=["ads"])


@router.post("", response_model=AdCreated, status_code=201)
def submit_ad(submission: AdSubmission):
    conn = postgres.connect()
    try:
        ad_id = postgres.insert_ad(
            conn,
            submission.advertiser_id,
            submission.headline,
            submission.body,
            str(submission.creative_url),
            submission.landing_domain,
        )
        conn.commit()
    except Exception as exc:  # noqa: BLE001
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"could not store ad: {exc}")
    finally:
        conn.close()

    # The ad is durably PENDING before we announce it; moderation is async.
    publish_ad_submitted(ad_id)
    return AdCreated(ad_id=ad_id, status="PENDING")
