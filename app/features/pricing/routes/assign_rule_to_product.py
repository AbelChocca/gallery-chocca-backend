from fastapi import Depends, status, Path
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service

@router.post(
    "/products/{product_id}/pricing-rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def assign_rule_to_product(
    product_id: Annotated[int, Path(...)],
    rule_id: Annotated[int, Path(...)],
    service: Annotated[PricingService, Depends(get_pricing_service)]
):
    await service.assign_rule_to_product(
        product_id=product_id,
        rule_id=rule_id
    )
    return None