from app.features.cart import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)