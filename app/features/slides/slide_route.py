from fastapi import APIRouter

router = APIRouter(prefix="/v1/slides", tags=["slides","v1"])

from app.features.slides.routes import delete_slide, get_slides, publish_slide, toggle_session, update_positions, update_slide