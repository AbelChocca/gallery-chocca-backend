from fastapi import Depends, status
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service

from app.features.pricing.schema import PricingRuleListResponse, PricingRuleFilterSchema, PricingRuleResponse
from app.shared.pagination.schema import PaginationSchema

@router.get(
    "/rules",
    status_code=status.HTTP_200_OK,
    response_model=PricingRuleListResponse
)
async def get_pricing_rules(
    filters: Annotated[PricingRuleFilterSchema, Depends()],
    pagination: Annotated[PaginationSchema, Depends()],
    service: Annotated[PricingService, Depends(get_pricing_service)]
):
    result = await service.get_pricing_rules(
        is_active=filters.is_active,
        type=filters.type,
        priority_min=filters.priority_min,
        priority_max=filters.priority_max,
        search=filters.search,
        limit=pagination.limit,
        page=pagination.page
    )

    return PricingRuleListResponse(
        total=result["total"],
        items=[
            PricingRuleResponse.model_validate(rule)
            for rule in result["items"]
        ],
        pagination=result["pagination"]
    )