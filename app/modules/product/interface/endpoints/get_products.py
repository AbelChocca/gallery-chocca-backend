from app.modules.product.interface.product_route import router
from app.modules.product.interface.schema.schema import ProductRead, FilterSchema, GetProductsResponse
from app.modules.product.interface.dependencies.case_depends import get_all_products_case
from app.modules.product.interface.schema.schema_mapper import ProductSchemaMapper
from app.modules.product.domain.use_cases.get_products import GetProductsCase

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
    filter_dto = ProductSchemaMapper.to_filter_dto(filter_schema)
    products = await case.execute(
        filter_dto, 
        offset, 
        limit
        )
    total_products = await case.count_products(filter_dto)
    return GetProductsResponse(
        total=total_products,
        productos=[
        ProductSchemaMapper.entity_to_schema(
            product
        )
        for product in products
    ]
    )
    
    