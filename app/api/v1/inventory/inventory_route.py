from fastapi import APIRouter

router = APIRouter(prefix="/v1/inventory", tags=["inventory"])

from app.api.v1.inventory.routes import create_movement, get_inventory_items, get_inventory_movements