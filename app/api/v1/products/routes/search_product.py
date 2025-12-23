from app.api.v1.products.product_route import router
from app.api.security.rate_limiter.ratelimiter import limiter
from app.api.schemas.products.schema import ProductRead
from app.api.dependencies.products.case_depends import get_search_products_case
from app.api.schemas.products.schema_mapper import OutputSchemaMapper

from app.application.products.cases.search_product import SearchProductCase

from fastapi import Depends, status, Query
from typing import List, Annotated

@router.post(
    path="/related/",
    dependencies=[Depends(limiter.limiter(limit=10, window=60))],
    status_code=status.HTTP_200_OK,
    summary="Returns realted product to query param",
    response_model=List[ProductRead]
)
async def search_product(
    query: Annotated[str, Query(min_length=2, title="Related title of Product's name")],
    case: Annotated[SearchProductCase, Depends(get_search_products_case)],
    offset: Annotated[int, Query(ge=0, lt=1)] = 0, # offset 0 for returns only the first three products of the related query
    limit: Annotated[int, Query(ge=0, le=3)] = 3,
) -> List[ProductRead]:
    res = await case.execute(query=query, offset=offset, limit=limit)
    return [
        OutputSchemaMapper.to_read_schema(dto=product)
        for product in res
    ]