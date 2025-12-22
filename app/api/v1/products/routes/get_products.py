from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import FilterSchema, GetProductsResponse
from app.api.dependencies.products.case_depends import get_all_products_case
from app.api.schemas.products.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.application.products.cases.get_products import GetProductsCase

from fastapi import status, Query, Depends, Body
from typing import Annotated

@router.post(
    "/all",
    response_model=GetProductsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all products"
)
async def get_products(
    filter_schema: Annotated[FilterSchema, Body()],
    case: Annotated[GetProductsCase, Depends(get_all_products_case)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20
) -> GetProductsResponse:
    filter_command = InputSchemaMapper.to_filter_command(filter_schema)
    res = await case.execute(
        filter_command, 
        offset, 
        limit
        )
    return GetProductsResponse(
        total=res.total,
        productos=[
        OutputSchemaMapper.to_read_schema(product)
        for product in res.products
    ]
    )
    
    