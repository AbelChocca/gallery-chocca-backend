from fastapi import Depends, status, Form

from app.features.inventory.inventory_route import router

from app.features.inventory.dependencies.services import (
    get_inventory_location_service,
)
from app.features.inventory.schemas.inventory_location_schema import (
    UpdateInventoryLocationSchema
)
from app.features.inventory.services.inventory_location_service import (
    InventoryLocationService,
)

@router.put(
    "/locations/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_inventory_location(
    location_id: int,
    body: UpdateInventoryLocationSchema = Form(...),
    service: InventoryLocationService = Depends(
        get_inventory_location_service,
    ),
) -> None:
    await service.update_location(
        location_id=location_id,
        name=body.name,
        type=body.type,
        address=body.address,
        is_active=body.is_active,
    )
