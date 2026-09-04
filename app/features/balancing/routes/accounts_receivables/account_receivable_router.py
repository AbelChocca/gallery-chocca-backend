from fastapi import APIRouter
from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission


accounts_receivable_router = APIRouter(
    prefix="/accounts-receivable",
    tags=["accounts-receivable"],
    dependencies=[require_permission(Permission.BALANCE_READ)]
)

from app.features.balancing.routes import accounts_receivables  # noqa: E402,F401