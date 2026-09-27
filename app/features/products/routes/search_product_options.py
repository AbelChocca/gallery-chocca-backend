from typing import Annotated

from fastapi import Depends, Query, status

from app.features.products.product_route import router
from app.features.products.service import ProductService
from app.features.products.dependency import get_product_service

from app.features.products.schema import (
    ProductSearchOptionResponseSchema,
)

from app.shared.pagination.schema import (
    PaginatedResponseSchema,
    PaginationResponseSchema,
)

@router.get(
    "/search-options",
    status_code=status.HTTP_200_OK,
)
async def search_product_options(
    service: Annotated[
        ProductService,
        Depends(get_product_service),
    ],
    search: Annotated[
        str | None,
        Query(
            min_length=2,
            max_length=100,
        ),
    ] = None,
    page: Annotated[
        int,
        Query(ge=1),
    ] = 1,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=50,
        ),
    ] = 20,
) -> PaginatedResponseSchema[
    ProductSearchOptionResponseSchema
]:
    products, total = (
        await service.search_product_options(
            search=search,
            page=page,
            limit=limit,
        )
    )

    total_pages = (
        total + limit - 1
    ) // limit

    return PaginatedResponseSchema[
        ProductSearchOptionResponseSchema
    ](
        items=[
            ProductSearchOptionResponseSchema.model_validate(
                product
            )
            for product in products
        ],
        total_items=total,
        pagination=PaginationResponseSchema(
            total_pages=total_pages,
            current_page=page,
        ),
    )