from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, JSON
from sqlmodel import Field, SQLModel

from app.features.payments.types.payment_provider import PaymentProvider

class PaymentEventTable(SQLModel, table=True):
    __tablename__ = "payment_events"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    payment_id: int | None = Field(
        default=None,
        foreign_key="payments.id",
        nullable=True,
        index=True,
    )

    provider: PaymentProvider = Field(
        nullable=False,
    )

    event_type: str = Field(
        max_length=100,
        nullable=False,
    )

    provider_event_id: str | None = Field(
        default=None,
        max_length=150,
        unique=True,
        index=True,
    )

    payload: dict = Field(
        sa_column=Column(
            JSON,
            nullable=False,
        ),
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )