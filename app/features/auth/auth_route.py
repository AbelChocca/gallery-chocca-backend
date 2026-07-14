from app.features.auth import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])