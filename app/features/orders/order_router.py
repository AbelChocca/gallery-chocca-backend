# app/features/checkout/checkout_route.py

from fastapi import APIRouter


router = APIRouter(
    prefix="/order",
    tags=["order"],
)


from app.features.orders.routes import order  # noqa: E402,F401