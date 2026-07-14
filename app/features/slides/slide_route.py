from app.features.slides import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix="/slides", tags=["slides"])