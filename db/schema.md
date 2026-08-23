# Moderation schema

Three tables, one append-only log.

| table               | purpose                                              |
| ------------------- | ---------------------------------------------------- |
| `advertisers`       | who submits ads                                      |
| `ads`               | one row per submission; `status` drives the workflow |
| `moderation_actions`| immutable audit trail — one row per decision         |

## The ad lifecycle

