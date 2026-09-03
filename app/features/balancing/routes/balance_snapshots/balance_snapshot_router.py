from fastapi import APIRouter

balance_router = APIRouter(
    prefix="/balance",
    tags=["balance"],
)

from app.features.balancing.routes import balance_snapshots  # noqa: E402,F401