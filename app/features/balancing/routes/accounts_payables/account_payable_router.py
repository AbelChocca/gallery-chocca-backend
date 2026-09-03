from fastapi import APIRouter

accounts_payable_router = APIRouter(
    prefix="/accounts-payable",
    tags=["accounts-payable"],
)

from app.features.balancing.routes import accounts_payables  # noqa: E402,F401