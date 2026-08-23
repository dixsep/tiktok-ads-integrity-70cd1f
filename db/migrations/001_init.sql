-- Core moderation data model.
-- Creatives are stored as URLs/keys for the MVP, not binary blobs.

CREATE TABLE advertisers (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT        NOT NULL,
    email       TEXT        NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TYPE ad_status AS ENUM ('PENDING', 'APPROVED', 'BLOCKED', 'REVIEW');

CREATE TABLE ads (
    id             BIGSERIAL PRIMARY KEY,
    advertiser_id  BIGINT      NOT NULL REFERENCES advertisers (id),
    headline       TEXT        NOT NULL,
    body           TEXT        NOT NULL,
    creative_url   TEXT        NOT NULL,
    landing_domain TEXT        NOT NULL,
    status         ad_status   NOT NULL DEFAULT 'PENDING',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- The most common reads: a single ad by id, an advertiser's ads,
-- and the review queue (a status slice ordered by time).
CREATE INDEX idx_ads_advertiser ON ads (advertiser_id);
CREATE INDEX idx_ads_status_created ON ads (status, created_at);

-- One immutable row per moderation action. We never UPDATE this table.
CREATE TABLE moderation_actions (
    id          BIGSERIAL PRIMARY KEY,
    ad_id       BIGINT      NOT NULL REFERENCES ads (id),
    actor_type  TEXT        NOT NULL,   -- SYSTEM | HUMAN
    actor_id    TEXT        NOT NULL,   -- moderation_worker | moderator email
    decision    ad_status   NOT NULL,   -- the status this action set
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_actions_ad ON moderation_actions (ad_id, created_at);
