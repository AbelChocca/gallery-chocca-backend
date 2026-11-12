from fastapi import APIRouter

router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
)

from app.features.locations.routes import ubigeo  # noqa: E402,F401