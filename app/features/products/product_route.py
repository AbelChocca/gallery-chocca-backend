from fastapi import APIRouter

router = APIRouter(prefix='/v1/product', tags=['products', 'v1'])

from app.features.products.routes import update_product, create_product, delete_product, get_product_by_id, get_products, search_product