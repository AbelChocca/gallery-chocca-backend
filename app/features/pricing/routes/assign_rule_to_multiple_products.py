from fastapi import Depends, status
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service
from app.features.pricing.schema import ProductRuleBatchRequest

@router.post(
    "/products/pricing-rules/assign-batch",
    status_code=status.HTTP_204_NO_CONTENT
)
async def assign_rule_to_products(
    payload: Annotated[ProductRuleBatchRequest, Depends()],
    service: Annotated[PricingService, Depends(get_pricing_service)]
):
    await service.assign_rule_to_products(
        product_ids=payload.product_ids,
        rule_id=payload.rule_id
    )
    return None