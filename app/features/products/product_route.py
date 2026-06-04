from fastapi import APIRouter

router = APIRouter(prefix='/product', tags=['products'])

from app.features.products.routes import update_product, create_product, delete_product, get_products, search_product, get_product_by_id