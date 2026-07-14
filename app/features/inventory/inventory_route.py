from fastapi import APIRouter

router = APIRouter(prefix="/inventory", tags=["inventory"])

from app.features.inventory import routes # noqa: E402,F401
