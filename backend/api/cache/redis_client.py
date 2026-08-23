"""Shared Redis connection for the API (read side of the cache)."""
import json
import os
import redis

_client: redis.Redis | None = None


def get_client() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.Redis.from_url(
            os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
            decode_responses=True,
        )
    return _client


def read_decision(ad_id: int) -> dict | None:
    raw = get_client().get(f"ad:decision:{ad_id}")
    return json.loads(raw) if raw else None
