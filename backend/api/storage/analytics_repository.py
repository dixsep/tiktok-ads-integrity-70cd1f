"""Postgres-driven analytics aggregations for the dashboard."""


def decision_counts(conn, days: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT status, count(*) AS n
              FROM ads
             WHERE created_at >= now() - (%s || ' days')::interval
             GROUP BY status
             ORDER BY n DESC
            """,
            (days,),
        )
        return cur.fetchall()


def top_rule_hits(conn, limit: int) -> list[dict]:
    # Unnest the JSONB rule_hits array, then count each rule id.
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT hit AS rule_id, count(*) AS n
              FROM ads, jsonb_array_elements_text(rule_hits) AS hit
             GROUP BY hit
             ORDER BY n DESC
             LIMIT %s
            """,
            (limit,),
        )
        return cur.fetchall()


def advertiser_risk(conn, limit: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT advertiser_id,
                   count(*)                                          AS ads,
                   round(avg(risk_score)::numeric, 3)                AS avg_risk,
                   round(avg((status = 'BLOCKED')::int)::numeric, 3) AS block_rate
              FROM ads
             WHERE risk_score IS NOT NULL
             GROUP BY advertiser_id
             ORDER BY block_rate DESC, avg_risk DESC
             LIMIT %s
            """,
            (limit,),
        )
        return cur.fetchall()
