-- Add the explainable moderation snapshot to ads, and let actions
-- carry the score detail that produced them.

ALTER TABLE ads
    ADD COLUMN risk_score   DOUBLE PRECISION,
    ADD COLUMN ml_score     DOUBLE PRECISION,
    ADD COLUMN rule_hits    JSONB NOT NULL DEFAULT '[]'::jsonb,
    ADD COLUMN reasons      JSONB NOT NULL DEFAULT '[]'::jsonb,
    ADD COLUMN moderated_at TIMESTAMPTZ;

ALTER TABLE moderation_actions
    ADD COLUMN risk_score DOUBLE PRECISION,
    ADD COLUMN detail     JSONB NOT NULL DEFAULT '{}'::jsonb;

-- GIN index lets us aggregate "top rule hits" over the JSONB array later.
CREATE INDEX idx_ads_rule_hits ON ads USING GIN (rule_hits);
