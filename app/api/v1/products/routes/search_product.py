from app.api.v1.products.product_route import router
from app.api.security.rate_limiter.ratelimiter import limiter
from app.api.schemas.products.schema import GridProductRead
from app.api.schemas.pagination import ProductRelatedPaginationSchema
from app.api.dependencies.products.case_depends import get_search_products_case

from app.application.products.cases.search_product import SearchProductCase

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
    case: Annotated[SearchProductCase, Depends(get_search_products_case)],
    pagination: Annotated[ProductRelatedPaginationSchema, Depends()]
) -> List[GridProductRead]:
    res = await case.execute(query, pagination.limit)
    return [
       GridProductRead(**product)
        for product in res
    ]