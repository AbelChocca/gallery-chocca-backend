from fastapi import APIRouter

router = APIRouter(prefix="/v1/dashboard", tags=['dashboard'])

from app.api.v1.dashboard.routes import overview

