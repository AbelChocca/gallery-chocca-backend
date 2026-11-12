
from typing import Annotated

from fastapi import Depends, status

from app.features.cart.cart_route import router

from app.features.cart.dependencies.services import (
    get_cart_service
)
from app.features.cart.service import CartService

from app.api.security.resolvers.session_owner import (
    OwnerSession,
    get_session_owner,
)


@router.get(
    "/count",
    status_code=status.HTTP_200_OK,
    summary="Get current cart items count",
)
async def get_cart_count(
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
    owner: Annotated[
        OwnerSession,
        Depends(get_session_owner),
    ],
) -> int:
    result = await service.get_active_cart_items_count(
        user_id=owner.user_id,
        session_id=owner.session_id,
    )

    return result
