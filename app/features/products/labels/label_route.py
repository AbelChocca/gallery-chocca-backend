from app.features.products.product_route import router

from fastapi import APIRouter

labels_route = APIRouter(prefix="/label", tags=["Product labels"])

from app.features.products.labels import routes # noqa: E402,F401

router.include_router(labels_route)