from fastapi import APIRouter

router = APIRouter(prefix="/favorites", tags=["favorites"])

from app.features.favorites import routes # noqa: E402,F401
