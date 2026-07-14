from fastapi import APIRouter

router = APIRouter(prefix='/product', tags=['products'])

from app.features.products import routes # noqa: E402,F401
