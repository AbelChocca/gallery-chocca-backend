from fastapi import APIRouter


financial_debt_router = APIRouter(
    prefix="/financial-debts",
    tags=["financial-debts"],
)

from app.features.balancing.routes import financial_debts  # noqa: E402,F401