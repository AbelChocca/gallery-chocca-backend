from fastapi import APIRouter

router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

from app.features.cart.routes import (
    add_item,
    decrement_item_quantity,
    get_cart,
    increment_item_quantity,
    remove_item,
    set_item_quantity,
    clear_cart
)