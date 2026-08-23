# TikTok | Ads Integrity & Content Moderation Platform

An intermediate capstone — design the Postgres data model for a moderation workflow, ingest ads through a REST API that persists then emits a Kafka event, run an event-driven moderation worker that combines an explainable rule engine with an ML risk classifier, persist an immutable audit trail, cache decisions in Redis for a real-time serving gate, expose moderation and override APIs, build a React review dashboard, and ship analytics over fraud patterns.

Built step-by-step with [KhwajaLabs Build](https://khwajalabs.com).

## Stack
- Python
- FastAPI
- Postgres
- Kafka
- Redis
- scikit-learn
- React
