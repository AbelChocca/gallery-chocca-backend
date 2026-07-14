from fastapi import APIRouter

router = APIRouter(prefix="/slides", tags=["slides"])

from app.features.slides import routes # noqa: E402,F401
