from app.features.products.product_route import router
from app.api.security.rate_limiter.ratelimiter import limiter
from app.features.products.schema import GridProductRead
from app.shared.pagination.schema import ProductRelatedPaginationSchema
from app.features.products.mappers.schema_mapper import OutputSchemaMapper
from app.features.products.dependency import get_related_products_use_case
from app.features.products.use_cases.search_product import GetRelatedProductsUseCase

from fastapi import Depends, status, Query
from typing import List, Annotated

@router.get(
    path="/related/",
    dependencies=[Depends(limiter.limiter(limit=25, window=30))],
    status_code=status.HTTP_200_OK,
    summary="Returns realted product to query param",
    response_model=List[GridProductRead]
)
async def search_product(
    query: Annotated[str, Query(min_length=2, title="Related title of Product's name")],
    use_case: Annotated[GetRelatedProductsUseCase, Depends(get_related_products_use_case)],
    pagination: Annotated[ProductRelatedPaginationSchema, Depends()]
) -> List[GridProductRead]:
    
    products = await use_case.execute(query, pagination.limit)

    return [
        OutputSchemaMapper.to_grid_product_read(product)
        for product in products
    ]