from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=['user'])

from app.features.user import routes # noqa: E402,F401
