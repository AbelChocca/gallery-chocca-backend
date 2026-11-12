from typing import Annotated

from fastapi import (
    Depends,
    Query,
    status,
)

from app.features.pricing.pricing_route import (
    router,
)

from app.features.pricing.schemas.promotion_schema import (
    PromotionFiltersSchema,
    PromotionRowResponseSchema,
)

from app.features.pricing.services.promotion import (
    PromotionService,
)

from app.features.pricing.dependencies.services.promotion import (
    get_promotion_service,
)

from app.shared.pagination.schema import (
    PaginatedResponseSchema,
)

from app.shared.datetime import (
    to_datetime_range,
)

from app.core.authorization.dependencies import (
    require_all_permissions,
)

from app.core.authorization.permissions import (
    Permission,
)


@router.get(
    "/promotions",
    status_code=status.HTTP_200_OK,
    dependencies=[
        require_all_permissions(
            Permission.PRICING_READ,
        )
    ],
)
async def get_promotions(
    filters: Annotated[
        PromotionFiltersSchema,
        Depends(),
    ],
    service: Annotated[
        PromotionService,
        Depends(get_promotion_service),
    ],
    page: Annotated[
        int,
        Query(
            ge=1,
        ),
    ] = 1,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
        ),
    ] = 20,
) -> PaginatedResponseSchema[
    PromotionRowResponseSchema
]:

    date_range = to_datetime_range(
        start=filters.starts_at,
        end=filters.ends_at,
    )

    result = await service.get_rows(
        page=page,
        limit=limit,
        search=filters.search,
        sales_channel=filters.sales_channel,
        starts_at=date_range.start,
        ends_at=date_range.end,
    )

    return PaginatedResponseSchema[
        PromotionRowResponseSchema
    ].model_validate(result)