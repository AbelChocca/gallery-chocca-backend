
from typing import Annotated

from fastapi import Depends, status

from app.features.favorites.favorites_router import router
from app.features.favorites.schema import FavoritesFilterSchema
from app.features.favorites.dto import FavoritesFilterDto

from app.features.favorites.use_cases.get_favorites_products import (
    GetFavoriteProductsUseCase,
)
from app.features.favorites.dependency import (
    get_favorite_products_use_case,
)

from app.features.products.schema import GetGridProductsResponse

from app.shared.pagination.schema import PaginationSchema

from app.api.security.resolvers.session_owner import (
    get_session_owner,
    OwnerSession,
)

from app.features.customer.dtos.customer import (
    CustomerPricingContext,
)
from app.features.customer.helpers.get_customer_pricing_context import (
    get_customer_pricing_context,
)


@router.get(
    path="/",
    response_model=GetGridProductsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get favorite products",
)
async def get_favorites_products(
    filter_body: Annotated[
        FavoritesFilterSchema,
        Depends(),
    ],
    pagination: Annotated[
        PaginationSchema,
        Depends(),
    ],
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
    use_case: Annotated[
        GetFavoriteProductsUseCase,
        Depends(get_favorite_products_use_case),
    ],
    customer: Annotated[
        CustomerPricingContext | None,
        Depends(get_customer_pricing_context),
    ],
) -> GetGridProductsResponse:

    res = await use_case.execute(
        filter=FavoritesFilterDto(
            **filter_body.model_dump()
        ),
        page=pagination.page,
        limit=pagination.limit,
        user_id=owner.user_id,
        session_id=owner.session_id,
        customer_id=(
            customer.customer_id
            if customer
            else None
        ),
        customer_type=(
            customer.customer_type
            if customer
            else None
        ),
    )

    return GetGridProductsResponse.model_validate(res)
