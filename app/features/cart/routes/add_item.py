from typing import Annotated

from fastapi import Depends, status

from app.features.cart.cart_route import router
from app.features.cart.dependency import get_cart_service
from app.features.cart.schema import AddCartItemRequest

from app.features.cart.service import CartService

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)

@router.post(
    path="/items",
    status_code=status.HTTP_201_CREATED,
    summary="Add item to cart",
)
async def add_item(
    body: AddCartItemRequest,
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    service: Annotated[CartService, Depends(get_cart_service)],
) -> None:
    await service.add_item(
        product_id=body.product_id,
        variant_id=body.variant_id,
        variant_size_id=body.variant_size_id,
        quantity=body.quantity,
        user_id=owner.user_id,
        session_id=owner.session_id,
    )