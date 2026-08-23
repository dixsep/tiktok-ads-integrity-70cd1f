"""API-side producer for override events (analytics consumes these)."""
import json
import os
from kafka import KafkaProducer

TOPIC_DECISION_OVERRIDDEN = "ad_decision_overridden"

_producer: KafkaProducer | None = None


def get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=os.environ.get("KAFKA_BROKERS", "localhost:9092"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: str(k).encode("utf-8"),
            acks="all",
        )
    return _producer


def publish_override(ad_id: int, decision: str, moderator: str) -> None:
    get_producer().send(
        TOPIC_DECISION_OVERRIDDEN,
        key=ad_id,
        value={"ad_id": ad_id, "decision": decision, "moderator": moderator},
    )
    get_producer().flush()
