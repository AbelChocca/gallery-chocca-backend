from app.shared.pagination.pagination_service import PaginationService

from app.features.balancing.entities.accounts_payable import AccountsPayable
from app.features.balancing.repositories.accounts_payable_repository import (
    AccountsPayableRepository,
)
from app.features.balancing.types.accounts_payable_types import (
    AccountsPayableCostCenter,
    AccountsPayableStatus,
    AccountsPayableUpdate
)
from app.core.exceptions import ValueNotFound

from datetime import datetime, timezone

class AccountsPayableService:

    def __init__(
        self,
        accounts_payable_repository: AccountsPayableRepository,
        pagination_service: PaginationService,
    ):
        self._accounts_payable_repository = accounts_payable_repository
        self._pagination_service = pagination_service

    async def create(
        self,
        entity: AccountsPayable,
    ) -> AccountsPayable:

        return await self._accounts_payable_repository.save(entity)

    async def update(
        self,
        entity_id: int,
        dto: AccountsPayableUpdate,
    ) -> AccountsPayable:

        entity = await self._accounts_payable_repository.get_by_id(entity_id)

        if entity is None:
            raise ValueNotFound(
                "No se pudo encontrar cuenta a pagar",
                {
                    "entity_id": entity_id
                }
            )

        if "brand" in dto.fields_set:
            entity.brand = dto.brand

        if "entity_name" in dto.fields_set:
            entity.entity_name = dto.entity_name

        if "cost_center" in dto.fields_set:
            entity.cost_center = dto.cost_center

        if "amount" in dto.fields_set:
            entity.amount = dto.amount

        if "status" in dto.fields_set:
            entity.status = dto.status

        entity.updated_at = datetime.now(timezone.utc)

        return await self._accounts_payable_repository.save(entity)

    async def get_by_id(
        self,
        account_payable_id: int,
    ) -> AccountsPayable:

        return await self._accounts_payable_repository.get_by_id(
            account_payable_id
        )

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        brand: str | None = None,
        cost_center: AccountsPayableCostCenter | None = None,
        status: AccountsPayableStatus | None = None,
    ) -> list[AccountsPayable]:

        return await self._accounts_payable_repository.find(
            balance_snapshot_id=balance_snapshot_id,
            brand=brand,
            cost_center=cost_center,
            status=status,
        )

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        brand: str | None = None,
        cost_center: AccountsPayableCostCenter | None = None,
        status: AccountsPayableStatus | None = None,
    ):
        return await self._accounts_payable_repository.sum_amount(
            balance_snapshot_id=balance_snapshot_id,
            brand=brand,
            cost_center=cost_center,
            status=status,
        )

    async def delete(
        self,
        account_payable_id: int,
    ) -> None:

        await self._accounts_payable_repository.delete_by_id(
            account_payable_id
        )