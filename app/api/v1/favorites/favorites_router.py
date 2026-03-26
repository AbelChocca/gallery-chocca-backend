from fastapi import APIRouter

router = APIRouter(prefix="/v1/favorites", tags=["favorites"])

from app.api.v1.favorites.routes import delete_favorite, get_favorites_products, get_status, set_favorite