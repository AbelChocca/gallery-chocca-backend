from fastapi import Depends, status
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service

@router.patch(
    "/rules/{rule_id}/activate",
    status_code=status.HTTP_204_NO_CONTENT
)
async def activate_pricing_rule(
    rule_id: int,
    service: Annotated[PricingService, Depends(get_pricing_service)]
):
    await service.activate_pricing_rule(rule_id=rule_id)
    return None