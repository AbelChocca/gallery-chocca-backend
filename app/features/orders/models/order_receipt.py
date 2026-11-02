from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum as SQLEnum
from sqlmodel import Field, SQLModel

from app.features.orders.types.order_receipt import ReceiptStatus


class OrderReceiptTable(SQLModel, table=True):
    __tablename__ = "order_receipts"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    order_id: int = Field(
        foreign_key="orders.id",
        nullable=False,
        unique=True,
        index=True,
    )

    status: ReceiptStatus = Field(
        default=ReceiptStatus.PENDING,
        sa_column=Column(
            SQLEnum(
                ReceiptStatus,
                values_callable=lambda enum: [e.value for e in enum],
                native_enum=False,
                create_constraint=True,
                name="ck_order_receipts_status",
            ),
            nullable=False,
        ),
    )

    external_id: str | None = Field(
        default=None,
        max_length=100,
        unique=True,
        index=True,
    )

    series_number: str | None = Field(
        default=None,
        max_length=30,
    )

    provider_error_code: str | None = Field(
        default=None,
        max_length=50,
    )

    provider_error_message: str | None = Field(
        default=None,
        max_length=500,
    )

    issued_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    email_sent_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    email_error_message: str | None = Field(
        default=None,
        max_length=500,
    )

    email_provider_id: str | None = Field(
        default=None,
        max_length=100,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )