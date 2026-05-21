from app.features.inventory.inventory_route import router
from app.features.inventory.inventory_schema import GetInventoryItemsResponse
from app.features.products.parsers import filter_dep
from app.features.products.schema import FilterSchema
from app.features.inventory.inventory_service import InventoryService
from app.features.inventory.dependency import get_inventory_service
from app.shared.pagination.schema import PaginationSchema
from app.features.products.schema_mapper import InputSchemaMapper

from fastapi import status, Depends
from typing import Annotated

@router.get(
    '/items',
    response_model=GetInventoryItemsResponse,
    status_code=status.HTTP_200_OK
)
async def get_inventory_items(
    filter_schema: Annotated[FilterSchema, Depends(filter_dep)],
    service: Annotated[InventoryService, Depends(get_inventory_service)],
    pagination: Annotated[PaginationSchema, Depends()]
) -> GetInventoryItemsResponse:
    filter_command = InputSchemaMapper.to_filter_command(filter_schema)
    result = await service.get_inventory_items(
        filter_command=filter_command,
        page=pagination.page,
        limit=pagination.limit
    )

    return GetInventoryItemsResponse(**result)

