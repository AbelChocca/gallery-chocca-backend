from app.features.products.product_route import router
from app.api.security.rate_limiter.ratelimiter import limiter
from app.features.products.schema import GridProductRead
from app.shared.pagination.schema import ProductRelatedPaginationSchema
from app.features.products.service import ProductService
from app.features.products.dependency import get_product_service

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
    service: Annotated[ProductService, Depends(get_product_service)],
    pagination: Annotated[ProductRelatedPaginationSchema, Depends()]
) -> List[GridProductRead]:
    res = await service.get_products_related(query, pagination.limit)
    return [
       GridProductRead(**product)
        for product in res
    ]