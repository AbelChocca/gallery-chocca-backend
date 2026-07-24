from fastapi import Depends, status, Form

from app.features.inventory.inventory_route import router

from app.features.inventory.dependencies.services import (
    get_inventory_location_service,
)
from app.features.inventory.schemas.inventory_location_schema import (
    CreateInventoryLocationSchema
)
from app.features.inventory.services.inventory_location_service import (
    InventoryLocationService,
)

@router.post(
    "/locations",
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory_location(
    body: CreateInventoryLocationSchema = Form(...),
    service: InventoryLocationService = Depends(
        get_inventory_location_service,
    ),
) -> None:
    await service.create_location(
        name=body.name,
        type=body.type,
        address=body.address,
    )