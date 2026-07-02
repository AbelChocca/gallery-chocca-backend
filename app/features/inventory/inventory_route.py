from fastapi import APIRouter

router = APIRouter(prefix="/inventory", tags=["inventory"])

from app.features.inventory.routes import get_inventory_movements, create_movement, create_bulk_movements