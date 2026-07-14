from app.features.user import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=['user'])