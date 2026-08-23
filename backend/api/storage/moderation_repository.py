"""Read-side queries for moderation details and the review queue."""


def get_ad_decision(conn, ad_id: int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, status, risk_score, ml_score, rule_hits, reasons, moderated_at "
            "FROM ads WHERE id = %s",
            (ad_id,),
        )
        return cur.fetchone()


def get_ad_detail(conn, ad_id: int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, advertiser_id, headline, body, creative_url, landing_domain, "
            "       status, risk_score, ml_score, rule_hits, reasons, moderated_at, created_at "
            "FROM ads WHERE id = %s",
            (ad_id,),
        )
        return cur.fetchone()


def list_by_status(conn, status: str, limit: int, offset: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, advertiser_id, headline, status, risk_score, created_at "
            "FROM ads WHERE status = %s "
            "ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (status, limit, offset),
        )
        return cur.fetchall()
