from app.features.inventory.inventory_service import InventoryService
from app.features.inventory.dto import CreateMovementCommand
from app.features.inventory.types import (
    InventoryOwnerType
)
from app.infra.cache.redis_service import RedisService
from app.features.inventory.resolvers.base import InventoryOwnerResolver
from app.features.inventory.constants import INVENTORY_MOVEMENTS_CACHE_KEY_TAG


class CreateMovementUseCase:
    def __init__(
        self,
        owner_resolvers: dict[
            InventoryOwnerType,
            InventoryOwnerResolver
        ],
        inventory_service: InventoryService,
        cache_service: RedisService
    ):
        self._owner_resolvers = owner_resolvers
        self._inventory_service = inventory_service
        self._cache_service = cache_service

    async def execute(
        self,
        command: CreateMovementCommand
    ) -> dict:
        resolver = self._owner_resolvers.get(
            command.owner_type
        )

        owner, previous_stock = await resolver.update_stock(
            command.owner_id,
            command.quantity,
            command.type
        )


        await self._inventory_service.create_movement(
            owner_type=InventoryOwnerType.MATERIAL,
            owner_id=owner.id,
            owner_name=owner.name,
            owner_code=owner.code,
            movement_type=command.type,
            quantity=abs(command.quantity), 
            prev_stock=previous_stock,
            new_stock=owner.stock,
            reason=command.reason
        )

        await self._cache_service.invalidate_entity(
            tag=resolver.cache_tag,
            entity_id=owner.id
        )

        await self._cache_service.invalidate_entities(
            INVENTORY_MOVEMENTS_CACHE_KEY_TAG
        )

        await self._cache_service.invalidate_entities(
            resolver.cache_tag
        )

        return {
            "message": "Material stock updated successfully."
        }