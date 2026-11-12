from fastapi import Depends

from app.features.inventory.inventory_route import router

from app.core.authorization.dependencies import (
    require_all_permissions,
)
from app.core.authorization.permissions import Permission

from app.features.inventory.schemas.inventory_location_schema import (
    InventoryLocationFiltersSchema,
    InventoryLocationResponseSchema,
)

from app.features.locations.services.location_service import LocationService
from app.features.locations.dependencies.services import get_location_service

@router.get(
    "/locations",
    response_model=list[InventoryLocationResponseSchema],
    dependencies=[
        require_all_permissions(
            Permission.INVENTORY_LOCATION_READ,
        )
    ],
)
async def get_inventory_locations(
    filters: InventoryLocationFiltersSchema = Depends(),
    service: LocationService = Depends(
        get_location_service,
    ),
):
    locations = await service.get_inventory_locations(
        search=filters.search,
        is_active=filters.is_active,
    )

    return [
        InventoryLocationResponseSchema.model_validate(location)
        for location in locations
    ]