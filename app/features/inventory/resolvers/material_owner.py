from app.features.material.service import MaterialService
from app.features.inventory.resolvers.base import InventoryOwnerResolver
from app.features.material.constants import MATERIAL_CACHE_KEY_TAG

from app.features.inventory.dto import (
    InventoryOwnerDTO,
    CreateBulkMovementCommand,
    UpdatedOwnerStockResult
)
from app.features.inventory.types import InventoryMovementType
from decimal import Decimal

class MaterialOwnerResolver(InventoryOwnerResolver):

    def __init__(
        self,
        material_service: MaterialService
    ):
        self._material_service = material_service

    async def update_stock(
        self,
        owner_id: int,
        quantity: Decimal,
        movement_type: InventoryMovementType
    ) -> tuple[InventoryOwnerDTO, int]:

        material, previous_stock = (
            await self._material_service.update_stock(
                material_id=owner_id,
                quantity=quantity,
                movement_type=movement_type
            )
        )

        return (
            InventoryOwnerDTO(
                id=material.id,
                stock=material.stock,
                name=material.name,
                code=material.code
            ),
            previous_stock
        )
    
    async def update_stock_many(
        self,
        command: CreateBulkMovementCommand
    ) -> list[UpdatedOwnerStockResult]:

        result = await (
            self._material_service.update_stock_many(
                material_ids=command.get_material_ids(),
                movement_type=command.type,
                movement_items=command.items
            )
        )

        return [
            UpdatedOwnerStockResult(
                owner_id=material.id,
                previous_stock=prev_stock,
                owner_code=material.code,
                new_stock=material.stock,
                owner_name=material.name
            )
            for material, prev_stock in result
        ]
    
    @property
    def cache_tag(self) -> str:
        return MATERIAL_CACHE_KEY_TAG