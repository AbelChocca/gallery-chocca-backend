from app.features.inventory.inventory_route import router
from app.features.inventory.inventory_schema import GetInventoryMovementsResponse, InventoryMovementFilterSchema
from app.features.inventory.inventory_service import InventoryService
from app.features.inventory.dependency import get_inventory_service
from app.shared.pagination.schema import PaginationSchema
from app.features.inventory.dto import InventoryMovementFilters

from fastapi import status, Depends
from typing import Annotated

@router.get(
    '/movements',
    response_model=GetInventoryMovementsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get inventory movements"
)
async def get_inventory_items(
    filter_schema: Annotated[InventoryMovementFilterSchema, Depends()],
    service: Annotated[InventoryService, Depends(get_inventory_service)],
    pagination: Annotated[PaginationSchema, Depends()]
) -> GetInventoryMovementsResponse:
    filter_command = InventoryMovementFilters(
        from_date=filter_schema.from_date,
        to_date=filter_schema.to_date,
        sku=filter_schema.sku,
        type=filter_schema.type
    )
    result = await service.get_inventory_movements(
        command=filter_command,
        page=pagination.page,
        limit=pagination.limit
    )

    return GetInventoryMovementsResponse(**result)

