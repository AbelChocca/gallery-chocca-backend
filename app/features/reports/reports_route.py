from fastapi import APIRouter

router = APIRouter(prefix='/reports', tags=['reports'])

from app.features.reports import routes # noqa: E402,F401
