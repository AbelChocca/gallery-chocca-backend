from app.features.inventory.types.inventory_movement import InventoryOwnerType
from app.features.inventory.resolvers.entity_resolver import EntityResolver

from app.features.inventory.dtos.inventory import InventoryOwnerDTO
from app.core.exceptions import UnsupportedEntity

class InventoryOwnerResolverService:

    def __init__(
        self,
        resolvers: dict[
            InventoryOwnerType,
            EntityResolver,
        ],
    ) -> None:
        self._resolvers = resolvers

    async def resolve(
        self,
        *,
        owner_type: InventoryOwnerType,
        owner_id: int,
    ) -> InventoryOwnerDTO:

        resolver = self._resolvers.get(owner_type)

        if resolver is None:
            raise UnsupportedEntity(
                "La entidad a resolver no esta soportada.",
                {
                    "owner_type": owner_type.value,
                    "owner_id": owner_id
                }
            )

        return await resolver.resolve(
            entity_id=owner_id,
        )