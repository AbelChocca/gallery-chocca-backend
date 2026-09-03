from app.features.balancing.entities.financial_debt import FinancialDebt
from app.features.balancing.repositories.financial_debt_repository import (
    FinancialDebtRepository,
)
from app.features.balancing.types.financial_debt_types import (
    FinancialDebtStatus,
    FinancialDebtUpdate
)
from app.core.exceptions import ValueNotFound

from datetime import datetime, timezone


class FinancialDebtService:

    def __init__(
        self,
        financial_debt_repository: FinancialDebtRepository,
    ):
        self._financial_debt_repository = financial_debt_repository

    async def create(
        self,
        entity: FinancialDebt,
    ) -> FinancialDebt:

        return await self._financial_debt_repository.save(entity)

    async def update(
        self,
        entity_id: int,
        dto: FinancialDebtUpdate,
    ) -> FinancialDebt:

        entity = await self._financial_debt_repository.get_by_id(entity_id)

        if entity is None:
            raise ValueNotFound(
                "No se pudo encontrar la deuda financiera",
                {
                    "entity_id": entity_id
                }
            )

        if "bank_name" in dto.fields_set:
            entity.bank_name = dto.bank_name

        if "amount" in dto.fields_set:
            entity.amount = dto.amount

        if "status" in dto.fields_set:
            entity.status = dto.status

        entity.updated_at = datetime.now(timezone.utc)

        return await self._financial_debt_repository.save(entity)

    async def get_by_id(
        self,
        financial_debt_id: int,
    ) -> FinancialDebt:

        return await self._financial_debt_repository.get_by_id(
            financial_debt_id
        )

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        bank_name: str | None = None,
        fiscal_year: int | None = None,
        status: FinancialDebtStatus | None = None,
    ) -> list[FinancialDebt]:

        return await self._financial_debt_repository.find(
            balance_snapshot_id=balance_snapshot_id,
            bank_name=bank_name,
            fiscal_year=fiscal_year,
            status=status,
        )

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        bank_name: str | None = None,
        fiscal_year: int | None = None,
        status: FinancialDebtStatus | None = None,
    ):
        return await self._financial_debt_repository.sum_amount(
            balance_snapshot_id=balance_snapshot_id,
            bank_name=bank_name,
            fiscal_year=fiscal_year,
            status=status,
        )

    async def delete(
        self,
        financial_debt_id: int,
    ) -> None:

        await self._financial_debt_repository.delete_by_id(
            financial_debt_id
        )