from fastapi import APIRouter
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

balance_router = APIRouter(
    prefix="/balance",
    tags=["balance"],
    dependencies=[require_permission(Permission.BALANCE_READ)]
)

from app.features.balancing.routes import balance_snapshots  # noqa: E402,F401