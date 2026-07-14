from fastapi import APIRouter

router = APIRouter(prefix='/pricing', tags=['pricing'])

from app.features.pricing import pricing_route # noqa: E402,F401
