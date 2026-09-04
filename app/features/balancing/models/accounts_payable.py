from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, Column, ForeignKey, func
from sqlmodel import Field, SQLModel

from app.features.balancing.types.accounts_payable_types import (
    AccountsPayableCostCenter,
    AccountsPayableStatus,
)


class AccountsPayableTable(SQLModel, table=True):
    __tablename__ = "accounts_payable"

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

    brand: str = Field(max_length=50, nullable=False)

    entity_name: str = Field(max_length=255, nullable=False)

    cost_center: AccountsPayableCostCenter | None = Field(
        default=None,
        sa_type=SAEnum(
            AccountsPayableCostCenter,
            name="accounts_payable_cost_center",
        ),
    )

    amount: Decimal = Field(
        max_digits=14,
        decimal_places=2,
        nullable=False,
    )

    status: AccountsPayableStatus = Field(
        sa_type=SAEnum(
            AccountsPayableStatus,
            name="accounts_payable_status",
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