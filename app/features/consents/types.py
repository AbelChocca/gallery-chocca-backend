from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum


class ConsentType(str, Enum):
    COOKIES = "COOKIES"
    TERMS = "TERMS"
    

@dataclass(frozen=True)
class CookiePreferencesDTO:
    analytics: bool
    marketing: bool


@dataclass(frozen=True)
class ConsentDTO:
    id: int
    consent_type: ConsentType
    version: str
    accepted: bool
    preferences: dict | None
    created_at: datetime


@dataclass(frozen=True)
class ConsentOwnerDTO:
    user_id: int | None
    session_id: UUID | None


@dataclass(frozen=True)
class ConsentSummaryDTO:
    cookies: ConsentDTO | None
    terms: ConsentDTO | None