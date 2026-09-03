from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, Column, ForeignKey, func
from sqlmodel import Field, SQLModel

from app.features.balancing.types.financial_debt_types import (
    FinancialDebtStatus,
)


class FinancialDebtTable(SQLModel, table=True):
    __tablename__ = "financial_debts"

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

    bank_name: str = Field(
        max_length=100,
        nullable=False,
    )

    amount: Decimal = Field(
        max_digits=14,
        decimal_places=2,
        nullable=False,
    )

    status: FinancialDebtStatus = Field(
        sa_type=SAEnum(
            FinancialDebtStatus,
            name="financial_debt_status",
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