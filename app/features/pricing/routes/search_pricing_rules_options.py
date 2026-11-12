from typing import Annotated

from fastapi import Depends, Query, status

from app.features.pricing.pricing_route import router
from app.features.pricing.dependencies.services.promotion_pricing_rule import (
    get_promotion_pricing_rule_service,
)
from app.features.pricing.services.promotion_pricing_rule import (
    PromotionPricingRuleService,
)
from app.features.pricing.schemas.pricing_rule_schema import (
    PricingRuleSearchOptionResponseSchema,
)

from app.shared.pagination.schema import (
    PaginatedResponseSchema,
    PaginationResponseSchema,
)
from app.core.authorization.dependencies import (
    require_permission,
)

from app.core.authorization.permissions import (
    Permission,
)
from app.api.security.rate_limiter.ratelimiter import limiter

@router.get(
    "/pricing-rules/search-options",
    response_model=PaginatedResponseSchema[
        PricingRuleSearchOptionResponseSchema
    ],
    dependencies=[
        require_permission(
            Permission.PRICING_READ
        )
        ,
        Depends(
            limiter.limiter(
                limit=30,
                window=30,
            )
        ),
    ],
    status_code=status.HTTP_200_OK,
    summary="Search pricing rules for selection",
)
async def search_pricing_rule_options(
    service: Annotated[
        PromotionPricingRuleService,
        Depends(get_promotion_pricing_rule_service),
    ],
    search: Annotated[
        str | None,
        Query(
            min_length=2,
            max_length=100,
            description="Search pricing rules by name or description.",
        ),
    ] = None,
    page: Annotated[
        int,
        Query(ge=1),
    ] = 1,
    limit: Annotated[
        int,
        Query(ge=1, le=50),
    ] = 20,
) -> PaginatedResponseSchema[
    PricingRuleSearchOptionResponseSchema
]:
    pricing_rules, total_items = await service.search_options(
        search=search,
        page=page,
        limit=limit,
    )

    total_pages = (
        total_items + limit - 1
    ) // limit

    return PaginatedResponseSchema[
        PricingRuleSearchOptionResponseSchema
    ](
        items=[
            PricingRuleSearchOptionResponseSchema.model_validate(
                pricing_rule
            )
            for pricing_rule in pricing_rules
        ],
        total_items=total_items,
        pagination=PaginationResponseSchema(
            current_page=page,
            total_pages=total_pages,
        ),
    )