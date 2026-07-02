from fastapi import APIRouter

router = APIRouter(prefix='/materials', tags=['material'])

from app.features.material.routes import activate_material, create_material, deactivate_material, get_material_by_id, get_materials, update_material