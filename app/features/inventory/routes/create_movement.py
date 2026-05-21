from app.features.inventory.inventory_route import router
from app.features.inventory.inventory_schema import CreateMovementSchema
from app.features.inventory.inventory_service import InventoryService
from app.features.inventory.dependency import get_inventory_service
from app.features.inventory.dto import CreateMovementCommand

from fastapi import Depends, status
from typing import Annotated

@router.post(
    '/movements/{variant_size_id}',
    status_code=status.HTTP_201_CREATED
)
async def create_movement(
    variant_size_id: int,
    schema: CreateMovementSchema,
    service: Annotated[InventoryService, Depends(get_inventory_service)]
) -> dict:
    command = CreateMovementCommand(
        variant_size_id=variant_size_id,
        product_id=schema.product_id,
        type=schema.type,
        quantity=schema.quantity,
        reason=schema.reason
    )
    return await service.create_movement(command)