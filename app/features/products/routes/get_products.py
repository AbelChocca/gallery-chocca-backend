from app.features.products.product_route import router
from app.features.products.schema import FilterSchema, GetGridProductsResponse
from app.features.products.schema_mapper import InputSchemaMapper
from app.shared.pagination.schema import PaginationSchema
from app.features.products.parsers import filter_dep
from app.features.products.service import ProductService
from app.features.products.dependency import get_product_service

from fastapi import status, Depends
from typing import Annotated

@router.get(
    "/all",
    response_model=GetGridProductsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all products"
)
async def get_products(
    filter_schema: Annotated[FilterSchema, Depends(filter_dep)],
    service: Annotated[ProductService, Depends(get_product_service)],
    pagination: Annotated[PaginationSchema, Depends()]
) -> GetGridProductsResponse:
    filter_command = InputSchemaMapper.to_filter_command(filter_schema)
    res = await service.get_products(
        filter_command, 
        pagination.page, 
        pagination.limit
        )
    return GetGridProductsResponse(**res)
    
    