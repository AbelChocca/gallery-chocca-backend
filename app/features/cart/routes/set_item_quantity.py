from typing import Annotated

from fastapi import Depends, status, Path, Query

from app.features.cart.cart_route import router
from app.features.cart.dependency import get_cart_service
from app.features.cart.service import CartService

@router.patch(
    path="/items/{cart_item_id}/quantity",
    status_code=status.HTTP_200_OK,
    summary="Set cart item quantity",
)
async def set_item_quantity(
    cart_item_id: Annotated[int, Path(...)],
    quantity: Annotated[int, Query(...)],
    service: Annotated[CartService, Depends(get_cart_service)],
) -> None:

    await service.set_item_quantity(
        cart_item_id=cart_item_id,
        quantity=quantity,
    )