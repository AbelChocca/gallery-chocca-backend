from fastapi import Depends

from app.features.material.service import MaterialService

from app.features.inventory.resolvers.material_owner import (
    MaterialOwnerResolver
)
from app.features.inventory.types import InventoryOwnerType
from app.features.inventory.resolvers.base import InventoryOwnerResolver

from app.features.material.dependency import (
    get_material_service
)


def get_material_owner_resolver(
    material_service: MaterialService = Depends(
        get_material_service
    )
) -> MaterialOwnerResolver:
    return MaterialOwnerResolver(
        material_service=material_service
    )

def get_inventory_owner_resolvers(
    material_resolver: MaterialOwnerResolver = Depends(
        get_material_owner_resolver
    )
) -> dict[
    InventoryOwnerType,
    InventoryOwnerResolver
]:

    return {
        InventoryOwnerType.MATERIAL:
            material_resolver
    }