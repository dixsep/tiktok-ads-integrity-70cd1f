"""Thin Postgres access layer for the API."""
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def connect():
    return psycopg2.connect(
        os.environ.get("DATABASE_URL", "postgresql://localhost/ads_integrity"),
        cursor_factory=RealDictCursor,
    )


def insert_ad(conn, advertiser_id: int, headline: str, body: str,
              creative_url: str, landing_domain: str) -> int:
    """Insert a PENDING ad and return its id. Caller controls the transaction."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ads (advertiser_id, headline, body, creative_url, landing_domain)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (advertiser_id, headline, body, creative_url, landing_domain),
        )
        return cur.fetchone()["id"]
