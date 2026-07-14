from app.features.products import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix='/product', tags=['products'])