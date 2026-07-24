from fastapi import Depends, status

from app.features.inventory.inventory_route import router

from app.features.inventory.dependencies.services import (
    get_inventory_location_service,
)
from app.features.inventory.schemas.inventory_location_schema import (
    ToggleInventoryLocationSchema
)
from app.features.inventory.services.inventory_location_service import (
    InventoryLocationService,
)

@router.patch(
    "/locations/{location_id}/toggle",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def toggle_inventory_location(
    location_id: int,
    body: ToggleInventoryLocationSchema,
    service: InventoryLocationService = Depends(
        get_inventory_location_service,
    ),
):
    await service.toggle_status(
        location_id=location_id,
        is_active=body.is_active,
    )