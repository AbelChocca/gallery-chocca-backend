from app.features.inventory.inventory_service import InventoryService

from app.features.inventory.dto import (
    CreateBulkMovementCommand
)

from app.features.inventory.types import (
    InventoryOwnerType
)

from app.infra.cache.redis_service import RedisService

from app.features.inventory.resolvers.base import InventoryOwnerResolver
from app.features.inventory.constants import INVENTORY_MOVEMENTS_CACHE_KEY_TAG


class CreateBulkMovementUseCase:
    def __init__(
        self,
        inventory_service: InventoryService,
        owner_resolvers: dict[
            InventoryOwnerType,
            InventoryOwnerResolver
        ],
        cache_service: RedisService
    ):
        self._owner_resolvers = owner_resolvers
        self._inventory_service = inventory_service
        self._cache_service = cache_service

    async def execute(
        self,
        command: CreateBulkMovementCommand
    ) -> dict:
        resolver = self._owner_resolvers.get(
            command.owner_type
        )
        
        result = await resolver.update_stock_many(command)

        quantities = command.get_quantities_by_owner_id()

        for item in result:
            quantity = quantities[item.owner_id]

            await self._inventory_service.create_movement(
                owner_type=command.owner_type,
                owner_id=item.owner_id,
                owner_code=item.owner_code,
                owner_name=item.owner_name,
                movement_type=command.type,
                quantity=abs(quantity),
                prev_stock=item.previous_stock,
                new_stock=item.new_stock,
                reason=command.reason
            )

        await self._cache_service.invalidate_entities(
            resolver.cache_tag
        )

        await self._cache_service.invalidate_entities(
            INVENTORY_MOVEMENTS_CACHE_KEY_TAG
        )

        return {
            "message": (
                "Materials updated successfully."
            )
        }