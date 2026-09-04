from app.features.balancing.entities.accounts_receivable import AccountsReceivable
from app.features.balancing.repositories.accounts_receivable_repository import (
    AccountsReceivableRepository,
)
from app.features.balancing.types.accounts_receivable_types import (
    AccountsReceivableStatus,
    AccountsReceivableUpdate
)
from app.core.exceptions import ValueNotFound

from datetime import datetime, timezone

class AccountsReceivableService:

    def __init__(
        self,
        accounts_receivable_repository: AccountsReceivableRepository,
    ):
        self._accounts_receivable_repository = (
            accounts_receivable_repository
        )

    async def create(
        self,
        entity: AccountsReceivable,
    ) -> AccountsReceivable:

        return await self._accounts_receivable_repository.save(
            entity
        )

    async def update(
        self,
        entity_id: int,
        dto: AccountsReceivableUpdate,
    ) -> AccountsReceivable:

        entity = await self._accounts_receivable_repository.get_by_id(entity_id)

        if entity is None:
            raise ValueNotFound(
                "No se pudo encontrar cuenta de recibo",
                {
                    "entity_id": entity_id
                }
            )

        if "brand" in dto.fields_set:
            entity.brand = dto.brand

        if "entity_name" in dto.fields_set:
            entity.entity_name = dto.entity_name

        if "location" in dto.fields_set:
            entity.location = dto.location

        if "amount" in dto.fields_set:
            entity.amount = dto.amount

        if "status" in dto.fields_set:
            entity.status = dto.status

        entity.updated_at = datetime.now(timezone.utc)

        return await self._accounts_receivable_repository.save(entity)

    async def get_by_id(
        self,
        account_receivable_id: int,
    ) -> AccountsReceivable:

        return await self._accounts_receivable_repository.get_by_id(
            account_receivable_id
        )

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        brand: str | None = None,
        entity_name: str | None = None,
        location: str | None = None,
        status: AccountsReceivableStatus | None = None,
    ) -> list[AccountsReceivable]:

        return await self._accounts_receivable_repository.find(
            balance_snapshot_id=balance_snapshot_id,
            brand=brand,
            entity_name=entity_name,
            location=location,
            status=status,
        )

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        brand: str | None = None,
        entity_name: str | None = None,
        location: str | None = None,
        status: AccountsReceivableStatus | None = None,
    ):
        return await self._accounts_receivable_repository.sum_amount(
            balance_snapshot_id=balance_snapshot_id,
            brand=brand,
            entity_name=entity_name,
            location=location,
            status=status,
        )

    async def delete(
        self,
        account_receivable_id: int,
    ) -> None:

        await self._accounts_receivable_repository.delete_by_id(
            account_receivable_id
        )