from typing import Annotated

from fastapi import Depends, status, Path

from app.features.cart.cart_route import router
from app.features.cart.dependency import get_cart_service
from app.features.cart.service import CartService


@router.delete(
    path="/items/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove item from cart",
)
async def remove_item(
    cart_item_id: Annotated[int, Path(...)],
    service: Annotated[CartService, Depends(get_cart_service)],
) -> None:
    await service.remove_item_from_cart(
        cart_item_id=cart_item_id,
    )