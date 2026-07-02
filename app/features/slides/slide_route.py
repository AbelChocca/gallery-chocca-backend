from fastapi import APIRouter

router = APIRouter(prefix="/slides", tags=["slides"])

from app.features.slides.routes import delete_slide, get_slides, publish_slide, toggle_session, update_positions, update_slide