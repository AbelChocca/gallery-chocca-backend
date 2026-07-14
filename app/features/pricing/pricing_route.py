from app.features.pricing import pricing_route # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix='/pricing', tags=['pricing'])