from fastapi import APIRouter


inventory_valuation_router = APIRouter(
    prefix="/inventory-valuations",
    tags=["inventory-valuations"],
)

from app.features.balancing.routes import inventory_valuation  # noqa: E402,F401
