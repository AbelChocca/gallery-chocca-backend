from fastapi import APIRouter

from app.features.favorites.routes import delete_favorite, get_favorites_products, get_status

router = APIRouter(prefix="/v1/favorites", tags=["favorites"])

from app.features.favorites.routes import set_favorite