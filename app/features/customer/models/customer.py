from app.features.customer.customer_types import IdentityDocumentType, CustomerType

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
                (user_id IS NOT NULL AND session_id IS NULL)
                OR
                (user_id IS NULL AND session_id IS NOT NULL)
            )
            """,
            name="ck_customer_identity",
        ),

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

    user_id: int | None = Field(
        default=None,
        foreign_key="usertable.id",
        unique=True,
        index=True,
    )

    session_id: str | None = Field(
        default=None,
        max_length=100,
        unique=True,
        index=True,
    )

    document_type: IdentityDocumentType | None = Field(
        default=None,
        sa_column=Column(
            ENUM(
                IdentityDocumentType,
                name="customer_document_type",
            ),
            nullable=True,
        ),
    )

    customer_type: CustomerType = Field(
        default=CustomerType.REGULAR,
        sa_column=Column(
            ENUM(
                CustomerType,
                name="customer_type",
            ),
            nullable=False,
        ),
    )

    document_number: str | None = Field(
        default=None,
        max_length=20,
        unique=True,
    )

    name: str = Field(
        max_length=100,
        nullable=False,
    )

    last_name: str = Field(
        max_length=100,
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