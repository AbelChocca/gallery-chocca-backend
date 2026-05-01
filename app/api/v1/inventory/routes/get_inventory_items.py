from app.api.v1.inventory.inventory_route import router
from app.api.schemas.inventory_schema import GetInventoryItemsResponse
from app.api.schemas.products.types import filter_dep
from app.api.schemas.products.schema import FilterSchema
from app.application.inventory_service import InventoryService
from app.api.dependencies.inventory_service import get_inventory_service
from app.api.schemas.pagination import PaginationSchema
from app.api.schemas.products.schema_mapper import InputSchemaMapper

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

