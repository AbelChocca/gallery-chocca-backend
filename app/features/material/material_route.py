from app.features.material import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix='/materials', tags=['material'])