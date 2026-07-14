from fastapi import APIRouter

router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

from app.features.cart import routes # noqa: E402,F401