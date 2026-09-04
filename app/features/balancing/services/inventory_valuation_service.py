from decimal import Decimal

from app.features.balancing.entities.inventory_valuation import (
    InventoryValuation,
)
from app.features.balancing.repositories.inventory_valuation_repository import (
    InventoryValuationRepository,
)
from app.features.balancing.types.inventory_valuation_types import (
    InventoryValuationCategory,
    InventoryValuationUpdate
)
from app.core.exceptions import ValueNotFound

from datetime import datetime, timezone


class InventoryValuationService:

    def __init__(
        self,
        inventory_valuation_repository: InventoryValuationRepository,
    ):
        self._inventory_valuation_repository = (
            inventory_valuation_repository
        )

    async def create(
        self,
        entity: InventoryValuation,
    ) -> InventoryValuation:

        return await self._inventory_valuation_repository.save(
            entity
        )

    async def update(
        self,
        entity_id: int,
        dto: InventoryValuationUpdate,
    ) -> InventoryValuation:

        entity = await self._inventory_valuation_repository.get_by_id(entity_id)

        if entity is None:
            raise ValueNotFound(
                "No se pudo encontrar la valuacion de inventario",
                {
                    "entity_id": entity_id
                }
            )

        if "category" in dto.fields_set:
            entity.category = dto.category

        if "subcategory" in dto.fields_set:
            entity.subcategory = dto.subcategory

        if "description" in dto.fields_set:
            entity.description = dto.description

        if "brand" in dto.fields_set:
            entity.brand = dto.brand

        if "location" in dto.fields_set:
            entity.location = dto.location

        if "quantity" in dto.fields_set:
            entity.quantity = dto.quantity

        if "unit_value" in dto.fields_set:
            entity.unit_value = dto.unit_value

        entity.updated_at = datetime.now(timezone.utc)

        return await self._inventory_valuation_repository.save(entity)

    async def get_by_id(
        self,
        inventory_valuation_id: int,
    ) -> InventoryValuation:

        return await self._inventory_valuation_repository.get_by_id(
            inventory_valuation_id
        )

    async def find(
        self,
        balance_snapshot_id: int | None = None,
        category: InventoryValuationCategory | None = None,
        subcategory: str | None = None,
        brand: str | None = None,
        location: str | None = None,
    ) -> list[InventoryValuation]:

        return await self._inventory_valuation_repository.find(
            balance_snapshot_id=balance_snapshot_id,
            category=category,
            subcategory=subcategory,
            brand=brand,
            location=location,
        )

    async def sum_amount(
        self,
        balance_snapshot_id: int | None = None,
        category: InventoryValuationCategory | None = None,
        subcategory: str | None = None,
        brand: str | None = None,
        location: str | None = None,
    ) -> Decimal:

        return await self._inventory_valuation_repository.sum_amount(
            balance_snapshot_id=balance_snapshot_id,
            category=category,
            subcategory=subcategory,
            brand=brand,
            location=location,
        )

    async def delete(
        self,
        inventory_valuation_id: int,
    ) -> None:

        await self._inventory_valuation_repository.delete_by_id(
            inventory_valuation_id
        )