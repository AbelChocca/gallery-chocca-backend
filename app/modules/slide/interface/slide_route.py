from fastapi import APIRouter


router = APIRouter(prefix="/slides", tags=["slides"])

from app.modules.slide.interface.endpoints import delete_slide, get_slides, publish_slide, update_slide