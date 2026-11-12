from fastapi import APIRouter


router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"],
)

from app.features.receipts import routes  # noqa: E402,F401