from fastapi import Depends, status
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service

from app.features.pricing.schema import (
    CreatePricingRuleRequest,
    PricingRuleResponse
)

@router.post(
    "/rules",
    status_code=status.HTTP_201_CREATED,
    response_model=PricingRuleResponse
)
async def create_pricing_rule(
    request: Annotated[CreatePricingRuleRequest, Depends()],
    service: Annotated[PricingService, Depends(get_pricing_service)]
):
    result = await service.create_pricing_rule(
        name=request.name,
        description=request.description,
        type=request.type,
        value=request.value,
        priority=request.priority,
        is_active=request.is_active,
        is_stackable=request.is_stackable
    )

    return PricingRuleResponse.model_validate(result)