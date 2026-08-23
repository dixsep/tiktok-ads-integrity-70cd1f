"""Moderation worker loop: consume -> moderate -> persist -> cache -> produce + commit."""
import logging
from datetime import datetime, timezone

from backend.moderation_worker.events.kafka_consumer import get_consumer
from backend.moderation_worker.events.kafka_producer import publish_ad_moderated
from backend.moderation_worker.storage import postgres
from backend.moderation_worker.storage.moderation_repository import save_moderation
from backend.moderation_worker.cache.cache_writer import write_decision
from backend.moderation_worker.pipeline.pipeline import run_pipeline

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("moderation-worker")


def handle(ad_id: int) -> None:
    conn = postgres.connect()
    try:
        ad = postgres.load_ad(conn, ad_id)
        if ad is None:
            log.warning("ad_id=%s not found, skipping", ad_id)
            return
        result = run_pipeline(ad)
        save_moderation(conn, ad_id, result.decision, result.risk_score,
                        ml_score=result.risk_score, rule_hits=result.rule_hits,
                        reasons=result.reasons)
        write_decision(ad_id, result.decision, result.risk_score,
                       datetime.now(timezone.utc).isoformat())
        publish_ad_moderated(ad_id, result.decision, result.risk_score)
        log.info("ad_id=%s decision=%s score=%.2f",
                 ad_id, result.decision, result.risk_score)
    finally:
        conn.close()


def main() -> None:
    consumer = get_consumer()
    log.info("moderation worker started")
    for message in consumer:
        ad_id = message.value["ad_id"]
        handle(ad_id)
        consumer.commit()


if __name__ == "__main__":
    main()
