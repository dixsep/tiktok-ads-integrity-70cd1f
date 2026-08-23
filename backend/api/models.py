"""Pydantic request/response models for the ads API."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class AdSubmission(BaseModel):
    advertiser_id: int
    headline: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=2000)
    creative_url: HttpUrl
    landing_domain: str = Field(min_length=1, max_length=255)


class AdCreated(BaseModel):
    ad_id: int
    status: str


class AdvertiserIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
