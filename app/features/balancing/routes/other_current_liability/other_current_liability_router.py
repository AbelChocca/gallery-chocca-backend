from fastapi import APIRouter


other_current_liability_router = APIRouter(
    prefix="/other-current-liabilities",
    tags=["other-current-liabilities"],
)

from app.features.balancing.routes import other_current_liability  # noqa: E402,F401