"""Kafka consumer for the moderation worker."""
import json
import os
from kafka import KafkaConsumer

TOPIC_AD_SUBMITTED = "ad_submitted"


def get_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        TOPIC_AD_SUBMITTED,
        bootstrap_servers=os.environ.get("KAFKA_BROKERS", "localhost:9092"),
        group_id="moderation-worker",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        # We commit offsets manually, only after a result is produced.
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )
