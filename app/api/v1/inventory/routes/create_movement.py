from app.api.v1.inventory.inventory_route import router
from app.api.schemas.inventory_schema import CreateMovementSchema
from app.application.inventory_service import InventoryService
from app.api.dependencies.inventory_service import get_inventory_service
from app.domain.inventory.data_models import CreateMovementCommand

from fastapi import Depends, status
from typing import Annotated

@router.post(
    '/movements/{variant_size_id}',
    status_code=status.HTTP_201_CREATED
)
async def create_movement(
    schema: Annotated[CreateMovementSchema, Depends()],
    service: Annotated[InventoryService, Depends(get_inventory_service)]
) -> dict:
    command = CreateMovementCommand(
        variant_size_id=schema.variant_size_id,
        product_id=schema.product_id,
        type=schema.type,
        quantity=schema.quantity,
        reason=schema.reason
    )
    return await service.create_movement(command)