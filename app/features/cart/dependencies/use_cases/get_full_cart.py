from fastapi import Depends

from app.features.cart.dependency import (
    get_cart_service,
)
from app.features.cart.service import (
    CartService,
)
from app.features.cart.use_cases.get_full_cart import (
    GetFullCartUseCase,
)
from app.features.pricing.dependencies.services.cart_pricing_service import (
    get_cart_pricing_service,
)
from app.features.pricing.services.cart_pricing import (
    CartPricingService,
)


def get_full_cart_use_case(
    cart_service: CartService = Depends(
        get_cart_service
    ),
    cart_pricing_service: CartPricingService = Depends(
        get_cart_pricing_service
    ),
) -> GetFullCartUseCase:
    return GetFullCartUseCase(
        cart_service=cart_service,
        cart_pricing_service=cart_pricing_service,
    )