"""FastAPI application entry point for the ads API."""
from fastapi import FastAPI

from backend.api.routes import ads

app = FastAPI(title="Ads Integrity API")
app.include_router(ads.router)


@app.get("/health")
def health():
    return {"status": "ok"}
