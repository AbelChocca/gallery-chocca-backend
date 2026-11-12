from fastapi import APIRouter

router = APIRouter(
    prefix="/payment/orders",
    tags=["Admin Orders - Payments"],
)

from app.features.payments import routes # noqa: E402,F401