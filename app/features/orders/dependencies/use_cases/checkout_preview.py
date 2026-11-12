from fastapi import Depends

from app.features.cart.dependencies.services import (
    get_cart_service,
)
from app.features.cart.service import (
    CartService,
)
from app.features.orders.use_cases.checkout_preview import (
    CheckoutPreviewUseCase,
)
from app.features.pricing.dependencies.services.sale_pricing_service import (
    get_sale_pricing_service,
)
from app.features.pricing.services.sale_pricing import (
    SalePricingService,
)
from app.features.locations.services.ubigeo_service import UbigeoService
from app.features.locations.dependencies.services import get_ubigeo_service,get_location_service
from app.features.locations.services.location_service import LocationService


def get_checkout_preview_use_case(
    cart_service: CartService = Depends(
        get_cart_service
    ),
    sale_pricing_service: SalePricingService = Depends(
        get_sale_pricing_service
    ),
    ubigeo_service: UbigeoService = Depends(
        get_ubigeo_service
    ),
    location_Service: LocationService = Depends(
        get_location_service
    )
) -> CheckoutPreviewUseCase:
    return CheckoutPreviewUseCase(
        cart_service=cart_service,
        sale_pricing_service=sale_pricing_service,
        ubigeo_service=ubigeo_service,
        location_service=location_Service
    )