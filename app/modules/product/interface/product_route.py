from fastapi import APIRouter


router = APIRouter(prefix='/product', tags=['products'])

from app.modules.product.interface.endpoints import get_products, delete_product, update_product, create_product, get_product_by_id, delete_image_product, delete_variant_product