from fastapi import APIRouter

from app.core.authorization.dependencies import require_permission
from app.core.authorization.permissions import Permission

accounts_payable_router = APIRouter(
    prefix="/accounts-payable",
    tags=["accounts-payable"],
    dependencies=[require_permission(Permission.BALANCE_READ)]
)

from app.features.balancing.routes import accounts_payables  # noqa: E402,F401