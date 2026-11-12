# app/features/checkout/checkout_route.py

from fastapi import APIRouter


router = APIRouter(
    prefix="/checkout",
    tags=["checkout"],
)


from app.features.orders.routes import checkout  # noqa: E402,F401