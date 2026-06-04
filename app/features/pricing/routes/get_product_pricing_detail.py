from fastapi import Depends, status, Path
from typing import Annotated

from app.features.pricing.pricing_route import router
from app.features.pricing.service import PricingService
from app.features.pricing.dependency import get_pricing_service

from app.features.pricing.schema import ProductPricingDetailResponse

@router.get(
    "/products/{product_id}/pricing-detail",
    status_code=status.HTTP_200_OK,
    response_model=ProductPricingDetailResponse
)
async def get_product_pricing_detail(
    product_id: Annotated[int, Path(...)],
    service: Annotated[PricingService, Depends(get_pricing_service)]
):
    result = await service.get_product_pricing_detail(product_id=product_id)

    return ProductPricingDetailResponse.model_validate(result)