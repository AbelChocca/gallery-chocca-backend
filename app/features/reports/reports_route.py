from app.features.reports import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix='/reports', tags=['reports'])