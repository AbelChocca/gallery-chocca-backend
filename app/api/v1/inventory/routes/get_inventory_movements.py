from app.api.v1.inventory.inventory_route import router
from app.api.schemas.inventory_schema import GetInventoryMovementsResponse, InventoryMovementFilterSchema
from app.application.inventory_service import InventoryService
from app.api.dependencies.inventory_service import get_inventory_service
from app.api.schemas.pagination import PaginationSchema
from app.domain.inventory.data_models import InventoryMovementFilters

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

