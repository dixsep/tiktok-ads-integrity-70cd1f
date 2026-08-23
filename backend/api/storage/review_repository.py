"""Apply a human override and append the audit action, atomically."""
import json

OVERRIDABLE_FROM = "REVIEW"
VALID_OVERRIDES = {"APPROVED", "BLOCKED"}


def apply_override(conn, ad_id: int, decision: str, moderator: str) -> bool:
    """Return True if the override applied, False if the ad wasn't in REVIEW."""
    if decision not in VALID_OVERRIDES:
        raise ValueError(f"illegal override {decision!r}")

    with conn.cursor() as cur:
        # Only an ad currently in REVIEW can be overridden — prevents
        # double-actions and racing moderators.
        cur.execute(
            "UPDATE ads SET status = %s, updated_at = now() "
            "WHERE id = %s AND status = %s",
            (decision, ad_id, OVERRIDABLE_FROM),
        )
        if cur.rowcount == 0:
            conn.rollback()
            return False

        cur.execute(
            "INSERT INTO moderation_actions "
            "    (ad_id, actor_type, actor_id, decision, detail) "
            "VALUES (%s, 'HUMAN', %s, %s, %s::jsonb)",
            (ad_id, moderator, decision,
             json.dumps({"override": True})),
        )
    conn.commit()
    return True
