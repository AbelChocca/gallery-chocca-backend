from app.features.dashboard import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=['dashboard'])