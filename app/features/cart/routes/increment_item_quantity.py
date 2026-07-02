from typing import Annotated

from fastapi import Depends, status, Path

from app.features.cart.cart_route import router
from app.features.cart.dependency import get_cart_service
from app.features.cart.service import CartService

@router.patch(
    path="/items/{cart_item_id}/increment",
    status_code=status.HTTP_200_OK,
    summary="Increment cart item quantity",
)
async def increment_item(
    cart_item_id: Annotated[int, Path(...)],
    service: Annotated[CartService, Depends(get_cart_service)],
) -> None:
    await service.increment_item_quantity(
        cart_item_id=cart_item_id,
    )