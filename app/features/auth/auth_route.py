from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])

from app.features.auth import routes # noqa: E402,F401