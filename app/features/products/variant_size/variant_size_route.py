from app.features.products.product_route import router

from fastapi import APIRouter

variant_size_router = APIRouter(prefix="/variant_size", tags=["Variant Size"])

router.include_router(variant_size_router)