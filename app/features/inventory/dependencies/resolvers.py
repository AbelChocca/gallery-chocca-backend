from app.features.material.dependency import get_material_service
from app.features.material.service import MaterialService
from app.features.inventory.resolvers.entities.material import MaterialEntityResolver
from app.features.inventory.resolvers.inventory_owner_resolver import InventoryOwnerResolverService
from app.features.inventory.types.inventory_movement import InventoryOwnerType

from fastapi import Depends



def get_material_entity_resolver(
    material_service: MaterialService = Depends(
        get_material_service,
    ),
) -> MaterialEntityResolver:
    return MaterialEntityResolver(
        material_service=material_service,
    )

def get_inventory_owner_resolver(
    material_entity_resolver: MaterialEntityResolver = Depends(
        get_material_entity_resolver,
    ),
) -> InventoryOwnerResolverService:
    return InventoryOwnerResolverService(
        resolvers={
            InventoryOwnerType.MATERIAL: material_entity_resolver,
        },
    )

