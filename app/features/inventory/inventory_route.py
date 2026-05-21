from fastapi import APIRouter

router = APIRouter(prefix="/v1/inventory", tags=["inventory"])

from app.features.inventory.routes import get_inventory_movements, create_movement, get_inventory_items