from app.api.v1.products.product_route import router
from app.api.schemas.products.schema import ProductRead, FilterSchema, GetProductsResponse
from app.api.dependencies.products.case_depends import get_all_products_case
from app.api.schemas.products.schema_mapper import InputSchemaMapper, OutputSchemaMapper
from app.application.products.cases.get_products import GetProductsCase

from fastapi import status, Query, Depends

@router.post(
    "/all",
    response_model=GetProductsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all products"
)
async def get_products(
    filter_schema: FilterSchema,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    case: GetProductsCase = Depends(get_all_products_case)
) -> GetProductsResponse:
    filter_command = InputSchemaMapper.to_filter_command(filter_schema)
    products = await case.execute(
        filter_command, 
        offset, 
        limit
        )
    total_products = await case.count_products(filter_command)
    return GetProductsResponse(
        total=total_products,
        productos=[
        OutputSchemaMapper.to_read_schema(product)
        for product in products
    ]
    )
    
    