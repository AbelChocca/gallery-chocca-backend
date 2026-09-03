from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, Column, ForeignKey, func
from sqlmodel import Field, SQLModel

from app.features.balancing.types.accounts_receivable_types import (
    AccountsReceivableStatus,
)
from app.shared.types import CompanyType

class AccountsReceivableTable(SQLModel, table=True):
    __tablename__ = "accounts_receivable"

    id: int | None = Field(default=None, primary_key=True)

    balance_snapshot_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "balance_snapshots.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        )
    )

    brand: CompanyType = Field(
        sa_column=Column(
            SAEnum(
                CompanyType,
                name="company_type"
            ),
            nullable=False
        )
    )

    entity_name: str = Field(max_length=255, nullable=False)

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    amount: Decimal = Field(
        max_digits=14,
        decimal_places=2,
        nullable=False,
    )

    status: AccountsReceivableStatus = Field(
        sa_type=SAEnum(
            AccountsReceivableStatus,
            name="accounts_receivable_status",
        ),
        nullable=False,
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )