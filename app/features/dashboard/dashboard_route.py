from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=['dashboard'])

from app.features.dashboard import routes # noqa: E402,F401
