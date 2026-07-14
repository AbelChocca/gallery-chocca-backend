from fastapi import APIRouter

router = APIRouter(prefix='/materials', tags=['material'])

from app.features.material import routes # noqa: E402,F401
