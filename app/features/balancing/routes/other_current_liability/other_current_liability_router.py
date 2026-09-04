from fastapi import APIRouter
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


other_current_liability_router = APIRouter(
    prefix="/other-current-liabilities",
    tags=["other-current-liabilities"],
    dependencies=[require_permission(Permission.BALANCE_READ)]
)

from app.features.balancing.routes import other_current_liability  # noqa: E402,F401