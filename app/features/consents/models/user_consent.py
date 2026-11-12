
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from app.features.consents.types import ConsentType


class UserConsentTable(SQLModel, table=True):
    __tablename__ = "user_consents"

    __table_args__ = (
        CheckConstraint(
            """
            (user_id IS NOT NULL AND session_id IS NULL)
            OR
            (user_id IS NULL AND session_id IS NOT NULL)
            """,
            name="ck_user_consents_owner",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    user_id: int | None = Field(
        default=None,
        foreign_key="usertable.id",
        nullable=True,
        index=True,
    )

    session_id: UUID | None = Field(
        default=None,
        nullable=True,
        index=True,
    )

    consent_type: ConsentType = Field(
        sa_column=Column(
            SQLEnum(
                ConsentType,
                values_callable=lambda enum: [
                    e.value for e in enum
                ],
                native_enum=False,
                create_constraint=True,
                name="ck_user_consents_type",
            ),
            nullable=False,
        ),
    )

    version: str = Field(
        max_length=20,
        nullable=False,
    )

    preferences: dict | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )

    accepted: bool = Field(
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
