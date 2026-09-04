from fastapi import APIRouter
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


financial_debt_router = APIRouter(
    prefix="/financial-debts",
    tags=["financial-debts"],
    dependencies=[require_permission(Permission.BALANCE_READ)]
)

from app.features.balancing.routes import financial_debts  # noqa: E402,F401