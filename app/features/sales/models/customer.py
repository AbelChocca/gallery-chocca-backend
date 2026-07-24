from app.features.sales.types.customer import CustomerDocumentType

from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlmodel import Field, SQLModel

class Customer(SQLModel, table=True):
    __tablename__ = "customer"

    __table_args__ = (
        CheckConstraint(
            """
            (
                (document_type IS NULL AND document_number IS NULL)
                OR
                (document_type IS NOT NULL AND document_number IS NOT NULL)
            )
            """,
            name="ck_customer_document_pair",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    document_type: CustomerDocumentType | None = Field(
        default=None,
        sa_column=Column(
            ENUM(
                CustomerDocumentType,
                name="customer_document_type",
                create_type=False,
            ),
            nullable=True,
        ),
    )

    document_number: str | None = Field(
        default=None,
        max_length=20,
        unique=True,
    )

    name: str = Field(
        max_length=150,
        nullable=False,
    )

    email: str | None = Field(
        default=None,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=lambda: datetime.now(timezone.utc)
    )