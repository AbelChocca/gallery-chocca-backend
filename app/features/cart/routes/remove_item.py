from typing import Annotated

from fastapi import Depends, status, Path

from app.features.cart.cart_route import router
from app.features.cart.dependencies.services import get_cart_service
from app.features.cart.service import CartService
from app.api.security.rate_limiter.ratelimiter import limiter
from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)

@router.delete(
    "/items/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(limiter.limiter(10, 60))],
    summary="Remove item from cart",
)
async def remove_item(
    cart_item_id: Annotated[int, Path(gt=0)],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
) -> None:
    await service.remove_item_from_cart(
        cart_item_id=cart_item_id,
        user_id=owner.user_id,
        session_id=owner.session_id,
    )
