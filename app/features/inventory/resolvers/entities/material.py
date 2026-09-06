from app.features.inventory.dtos.inventory import InventoryOwnerDTO
from app.features.inventory.resolvers.entity_resolver import EntityResolver

from app.features.material.service import MaterialService

from app.core.exceptions import ValueNotFound


class MaterialEntityResolver(EntityResolver):

    def __init__(
        self,
        material_service: MaterialService,
    ) -> None:
        self._material_service = material_service

    async def resolve(
        self,
        *,
        entity_id: int,
    ) -> InventoryOwnerDTO:

        material = await self._material_service.get_by_id(
            entity_id
        )

        if material is None:
            raise ValueNotFound(
                "El material no fue encuentra",
                {
                    "material_id": entity_id
                }
            )

        return InventoryOwnerDTO(
            id=material.id,
            unit_type=material.unit_type,
        )