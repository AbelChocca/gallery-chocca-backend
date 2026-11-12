from fastapi import APIRouter

router = APIRouter(
    prefix="/consents",
    tags=["consents"],
)

from app.features.consents import routes  # noqa: E402,F401