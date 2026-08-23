"""Kafka producer for the moderation worker's results."""
import json
import os
from kafka import KafkaProducer

TOPIC_AD_MODERATED = "ad_moderated"

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


def publish_ad_moderated(ad_id: int, decision: str, risk_score: float) -> None:
    get_producer().send(
        TOPIC_AD_MODERATED,
        key=ad_id,
        value={"ad_id": ad_id, "decision": decision, "risk_score": risk_score},
    )
    get_producer().flush()
