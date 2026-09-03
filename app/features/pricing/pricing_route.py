from fastapi import APIRouter

router = APIRouter(prefix='/pricing', tags=['pricing'])

from app.features.pricing import routes # noqa: E402,F401
