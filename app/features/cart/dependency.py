from fastapi import Depends
from app.features.cart.service import CartService

from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork


def get_cart_service(
    uow: UnitOfWork = Depends(get_uow),
) -> CartService:

    return CartService(
        cart_repository=uow.carts,
        product_repository=uow.products,
        product_pricing_repository=uow.product_pricing,
    )