from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.features.consents.types import ConsentType

class PolicyVersionsResponse(BaseModel):
    terms: str
    privacy: str
    cookies: str

class CookiePreferencesSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analytics: bool
    marketing: bool


class SaveCookieConsentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preferences: CookiePreferencesSchema


class ConsentResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    consent_type: ConsentType
    version: str
    accepted: bool
    preferences: dict | None
    created_at: datetime


class ConsentSummaryResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cookies: ConsentResponseSchema | None
    terms: ConsentResponseSchema | None