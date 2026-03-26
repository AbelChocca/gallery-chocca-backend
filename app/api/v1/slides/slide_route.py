from fastapi import APIRouter

router = APIRouter(prefix="/v1/slides", tags=["slides","v1"])

from app.api.v1.slides.routes import update_orders, delete_slide, get_slides, publish_slide, update_slide