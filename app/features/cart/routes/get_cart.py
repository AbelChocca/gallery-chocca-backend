from typing import Annotated

from fastapi import Depends, status

from app.features.cart.cart_route import router
from app.features.cart.dependency import get_cart_service
from app.features.cart.service import CartService

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)

from app.features.cart.schema import CartResponse


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Get active cart"
)
async def get_cart(
    owner: Annotated[OwnerSession, Depends(get_session_owner)],
    service: Annotated[CartService, Depends(get_cart_service)],
) -> CartResponse | None:
    result = await service.get_full_cart_by_owner(
        user_id=owner.user_id,
        session_id=owner.session_id,
    )

    return (
        CartResponse(**result) 
        if result is not None 
        else CartResponse(
            items=[],
            subtotal=0,
            total=0,
            total_items=0,
            cart_id=None
        )
    )