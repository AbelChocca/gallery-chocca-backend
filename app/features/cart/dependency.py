from fastapi import Depends
from app.features.cart.service import CartService
from app.features.pricing.utils.pricing_calculator import ProductPricingCalculator, get_pricing_calculator

from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork


def get_cart_service(
    uow: UnitOfWork = Depends(get_uow),
    pricing_calculator: ProductPricingCalculator = Depends(get_pricing_calculator)
) -> CartService:

    return CartService(
        cart_repository=uow.carts,
        product_repository=uow.products,
        product_pricing_repository=uow.product_pricing,
        pricing_calculator=pricing_calculator
    )