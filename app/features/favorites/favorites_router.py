from fastapi import APIRouter

router = APIRouter(prefix="/favorites", tags=["favorites"])

from app.features.favorites.routes import set_favorite, delete_favorite, get_favorites_products, get_status