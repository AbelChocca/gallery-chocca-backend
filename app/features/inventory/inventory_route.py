from app.features.inventory import routes # noqa: F401

from fastapi import APIRouter

router = APIRouter(prefix="/inventory", tags=["inventory"])