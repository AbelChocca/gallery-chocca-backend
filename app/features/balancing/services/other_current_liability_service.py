from decimal import Decimal

from app.features.balancing.entities.other_current_liability import (
    OtherCurrentLiability,
)
from app.features.balancing.repositories.other_current_liability_repository import (
    OtherCurrentLiabilityRepository,
)
from app.features.balancing.types.other_current_liability_types import (
    OtherCurrentLiabilityStatus,
    OtherCurrentLiabilityUpdate,
    OtherCurrentLiabilityCategory
)
from app.core.exceptions import ValueNotFound

from datetime import datetime, timezone


class OtherCurrentLiabilityService:

    def __init__(
        self,
        other_current_liability_repository: OtherCurrentLiabilityRepository,
    ):
        self._other_current_liability_repository = (
            other_current_liability_repository
        )

    async def create(
        self,
        entity: OtherCurrentLiability,
    ) -> OtherCurrentLiability:

        return await self._other_current_liability_repository.save(
            entity
        )
    async def update(
        self,
        entity_id: int,
        dto: OtherCurrentLiabilityUpdate,
    ) -> OtherCurrentLiability:

        entity = await self._other_current_liability_repository.get_by_id(entity_id)

        if entity is None:
            raise ValueNotFound(
                "No se pudo encontrar la responsabilidad",
                {
                    "entity_id": entity_id
                }
            )

        if "category" in dto.fields_set:
            entity.category = dto.category

        if "description" in dto.fields_set:
            entity.description = dto.description

        if "amount" in dto.fields_set:
            entity.amount = dto.amount

        if "status" in dto.fields_set:
            entity.status = dto.status

        entity.updated_at = datetime.now(timezone.utc)

        return await self._other_current_liability_repository.save(entity)

    async def get_by_id(
        self,
        other_current_liability_id: int,
    ) -> OtherCurrentLiability:

        return await self._other_current_liability_repository.get_by_id(
            other_current_liability_id
        )

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        category: OtherCurrentLiabilityCategory | None = None,
        status: OtherCurrentLiabilityStatus | None = None,
    ) -> list[OtherCurrentLiability]:

        return await self._other_current_liability_repository.find(
            balance_snapshot_id=balance_snapshot_id,
            category=category,
            status=status,
        )

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        category: str | None = None,
        status: OtherCurrentLiabilityStatus | None = None,
    ) -> Decimal:

        return await self._other_current_liability_repository.sum_amount(
            balance_snapshot_id=balance_snapshot_id,
            category=category,
            status=status,
        )

    async def delete(
        self,
        other_current_liability_id: int,
    ) -> None:

        await self._other_current_liability_repository.delete_by_id(
            other_current_liability_id
        )