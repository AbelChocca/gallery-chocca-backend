from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=['dashboard'])

from app.features.dashboard.routes import overview

