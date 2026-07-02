from fastapi import Depends, status
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service

from app.features.pricing.schema import (
    ProductsPricingRulesResponse,
    ProductAppliedPricingRuleResponse,
)
from app.shared.pagination.schema import PaginationSchema

@router.get(
    "/products/{product_id}/pricing-rules",
    status_code=status.HTTP_200_OK,
    response_model=ProductsPricingRulesResponse
)
async def get_product_pricing_rules(
    product_id: int,
    pagination: Annotated[PaginationSchema, Depends()],
    service: Annotated[PricingService, Depends(get_pricing_service)] = None
):
    result = await service.get_product_pricing_rules(
        product_id=product_id,
        page=pagination.page,
        limit=pagination.limit
    )

    return ProductsPricingRulesResponse(
        total_items=result["total_items"],
        items=[
            ProductAppliedPricingRuleResponse.model_validate(rule)
            for rule in result["items"]
        ],
        pagination=result["pagination"]
    )