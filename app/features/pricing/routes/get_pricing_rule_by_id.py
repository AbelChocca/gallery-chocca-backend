from fastapi import Depends, status, Path
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service

from app.features.pricing.schema import PricingRuleResponse

@router.get(
    "/rules/{rule_id}",
    status_code=status.HTTP_200_OK,
    response_model=PricingRuleResponse
)
async def get_pricing_rule(
    rule_id: Annotated[int, Path(...)],
    service: Annotated[PricingService, Depends(get_pricing_service)]
):
    result = await service.get_pricing_rule(rule_id=rule_id)

    return PricingRuleResponse.model_validate(result)