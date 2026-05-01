from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import FilterSchema, GetGridProductsResponse
from app.api.dependencies.products.case_depends import get_all_products_case
from app.api.schemas.products.schema_mapper import InputSchemaMapper
from app.api.schemas.pagination import PaginationSchema
from app.application.products.cases.get_products import GetProductsCase
from app.api.schemas.products.types import filter_dep

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
    case: Annotated[GetProductsCase, Depends(get_all_products_case)],
    pagination: Annotated[PaginationSchema, Depends()]
) -> GetGridProductsResponse:
    filter_command = InputSchemaMapper.to_filter_command(filter_schema)
    res = await case.execute(
        filter_command, 
        pagination.page, 
        pagination.limit
        )
    return GetGridProductsResponse(**res)
    
    