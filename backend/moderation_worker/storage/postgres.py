"""Postgres access for the moderation worker."""
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def connect():
    return psycopg2.connect(
        os.environ.get("DATABASE_URL", "postgresql://localhost/ads_integrity"),
        cursor_factory=RealDictCursor,
    )


def load_ad(conn, ad_id: int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, advertiser_id, headline, body, creative_url, landing_domain, status "
            "FROM ads WHERE id = %s",
            (ad_id,),
        )
        return cur.fetchone()
