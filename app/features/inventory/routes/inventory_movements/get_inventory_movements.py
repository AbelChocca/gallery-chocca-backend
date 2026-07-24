from app.features.inventory.inventory_route import router
from app.features.inventory.schemas.inventory_movement_schema import GetInventoryMovementsResponse, InventoryMovementFilterSchema
from app.features.inventory.use_cases.get_inventory_movements import (
    GetInventoryMovementsUseCase
)
from app.features.inventory.dependencies.inventory_movements_cases import (
    get_inventory_movements_use_case
)
from app.shared.pagination.schema import PaginationSchema
from app.features.inventory.dtos.inventory_movements import InventoryMovementFilters
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission
from app.shared.datetime import to_datetime_range

from fastapi import status, Depends
from typing import Annotated

@router.get(
    '/movements',
    response_model=GetInventoryMovementsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get inventory movements",
    dependencies=[
        require_permission(Permission.INVENTORY_READ)
    ]
)
async def get_inventory_movements(
    filter_schema: Annotated[InventoryMovementFilterSchema, Depends()],
    pagination: Annotated[PaginationSchema, Depends()],
    use_case: Annotated[
        GetInventoryMovementsUseCase,
        Depends(get_inventory_movements_use_case)
    ]
) -> GetInventoryMovementsResponse:
    datetime_range = to_datetime_range(filter_schema.from_date, filter_schema.to_date)
    filters = InventoryMovementFilters(
        from_date=datetime_range.start,
        to_date=datetime_range.end,
        search=filter_schema.search,
        owner_type=filter_schema.owner_type,
        type=filter_schema.type,
        owner_id=filter_schema.owner_id
    )
    result = await use_case.execute(
        filters=filters,
        page=pagination.page,
        limit=pagination.limit
    )

    return GetInventoryMovementsResponse(
        **result.to_dict()
    )

