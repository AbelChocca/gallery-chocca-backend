from app.features.products.product_route import router
from app.features.products.schema import FilterSchema, GetGridProductsResponse
from app.features.products.mappers.schema_mapper import InputSchemaMapper
from app.shared.pagination.schema import PaginationSchema
from app.features.products.parsers import filter_dep
from app.features.products.dependency import get_products_use_case
from app.features.products.use_cases.get_products import GetProductsUseCase

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
    use_case: Annotated[GetProductsUseCase, Depends(get_products_use_case)],
    pagination: Annotated[PaginationSchema, Depends()]
) -> GetGridProductsResponse:
    
    filter_command = InputSchemaMapper.to_filter_command(filter_schema)

    res = await use_case.execute(
        filter_command,
        pagination.page,
        pagination.limit
    )

    return GetGridProductsResponse.model_validate(res)
    
    