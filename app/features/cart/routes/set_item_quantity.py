from typing import Annotated

from fastapi import Depends, status, Path, Query

from app.features.cart.cart_route import router
from app.features.cart.dependencies.services import get_cart_service
from app.features.cart.service import CartService
from app.api.security.rate_limiter.ratelimiter import limiter
from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)

@router.patch(
    "/items/{cart_item_id}/quantity",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(limiter.limiter(10, 60))],
    summary="Set cart item quantity",
)
async def set_item_quantity(
    cart_item_id: Annotated[int, Path(gt=0)],
    quantity: Annotated[int, Query(gt=0)],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
) -> None:
    await service.set_item_quantity(
        cart_item_id=cart_item_id,
        quantity=quantity,
        user_id=owner.user_id,
        session_id=owner.session_id,
    )
