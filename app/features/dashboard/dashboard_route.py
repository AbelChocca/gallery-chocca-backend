from fastapi import APIRouter

router = APIRouter(prefix="/v1/dashboard", tags=['dashboard'])

from app.features.dashboard.routes import overview

