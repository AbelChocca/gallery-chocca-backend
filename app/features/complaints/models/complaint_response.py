
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Text
from sqlmodel import Field, SQLModel

from app.features.complaints.types.complaint_response import (
    ComplaintResponseStatus,
)


class ComplaintResponseTable(SQLModel, table=True):
    __tablename__ = "complaint_responses"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    complaint_id: int = Field(
        foreign_key="complaints.id",
        nullable=False,
        index=True,
    )

    author_user_id: int | None = Field(
        default=None,
        foreign_key="usertable.id",  # Ajustar al nombre real
    )

    message: str = Field(
        sa_column=Column(Text, nullable=False),
    )

    status: ComplaintResponseStatus = Field(
        default=ComplaintResponseStatus.DRAFT,
        sa_column=Column(
            SQLEnum(
                ComplaintResponseStatus,
                values_callable=lambda enum: [
                    e.value for e in enum
                ],
                native_enum=False,
                create_constraint=True,
                name="ck_complaint_responses_status",
            ),
            nullable=False,
            server_default=ComplaintResponseStatus.DRAFT.value,
        ),
    )

    recipient_email: str | None = Field(
        default=None,
        max_length=320,
    )

    external_message_id: str | None = Field(
        default=None,
        max_length=255,
        index=True,
    )

    error_message: str | None = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )

    # Para respuesta física, si corresponde
    physical_delivery_reference: str | None = Field(
        default=None,
        max_length=255,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    sent_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )

    delivered_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )
