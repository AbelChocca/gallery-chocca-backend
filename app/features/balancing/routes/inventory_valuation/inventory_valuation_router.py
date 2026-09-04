from fastapi import APIRouter
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


inventory_valuation_router = APIRouter(
    prefix="/inventory-valuations",
    tags=["inventory-valuations"],
    dependencies=[require_permission(Permission.BALANCE_READ)]
)

from app.features.balancing.routes import inventory_valuation  # noqa: E402,F401
