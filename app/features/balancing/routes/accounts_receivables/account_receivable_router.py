from fastapi import APIRouter


accounts_receivable_router = APIRouter(
    prefix="/accounts-receivable",
    tags=["accounts-receivable"],
)

from app.features.balancing.routes import accounts_receivables  # noqa: E402,F401