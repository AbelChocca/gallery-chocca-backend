from app.features.favorites import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix="/favorites", tags=["favorites"])