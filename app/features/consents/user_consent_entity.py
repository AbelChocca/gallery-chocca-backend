from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID

from app.features.consents.types import ConsentType


@dataclass
class UserConsentEntity:
    user_id: int | None
    session_id: UUID | None

    consent_type: ConsentType
    version: str
    accepted: bool

    preferences: dict | None = None

    id: int | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )