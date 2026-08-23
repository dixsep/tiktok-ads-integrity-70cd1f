"""Persist a moderation result: snapshot on the ad + immutable action row.

Both writes happen in one transaction so the ad's status and its audit log can
never disagree.
"""
import json

VALID_DECISIONS = {"APPROVED", "BLOCKED", "REVIEW"}


def save_moderation(conn, ad_id: int, decision: str, risk_score: float,
                    ml_score: float, rule_hits: list[str],
                    reasons: list[str]) -> None:
    if decision not in VALID_DECISIONS:
        raise ValueError(f"illegal decision {decision!r}")

    with conn.cursor() as cur:
        # Only transition an ad that is still PENDING — never clobber a
        # human override that may have already moved it.
        cur.execute(
            """
            UPDATE ads
               SET status = %s,
                   risk_score = %s,
                   ml_score = %s,
                   rule_hits = %s::jsonb,
                   reasons = %s::jsonb,
                   moderated_at = now(),
                   updated_at = now()
             WHERE id = %s AND status = 'PENDING'
            """,
            (decision, risk_score, ml_score,
             json.dumps(rule_hits), json.dumps(reasons), ad_id),
        )
        if cur.rowcount == 0:
            conn.rollback()
            return  # already moderated/overridden; nothing to do

        cur.execute(
            """
            INSERT INTO moderation_actions
                (ad_id, actor_type, actor_id, decision, risk_score, detail)
            VALUES (%s, 'SYSTEM', 'moderation_worker', %s, %s, %s::jsonb)
            """,
            (ad_id, decision, risk_score,
             json.dumps({"rule_hits": rule_hits, "reasons": reasons,
                         "ml_score": ml_score})),
        )
    conn.commit()
