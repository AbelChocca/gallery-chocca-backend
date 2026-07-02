from typing import Annotated

from fastapi import Depends, Path, status

from app.features.cart.cart_route import router
from app.features.cart.dependency import get_cart_service
from app.features.cart.service import CartService


@router.delete(
    path="/{cart_id}/clear",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear cart",
)
async def clear_cart(
    cart_id: Annotated[int, Path(gt=0)],
    service: Annotated[CartService, Depends(get_cart_service)],
) -> None:
    await service.clear_cart(
        cart_id=cart_id,
    )