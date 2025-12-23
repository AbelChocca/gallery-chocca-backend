from fastapi import APIRouter


router = APIRouter(prefix='/v1/product', tags=['products', 'v1'])

from app.api.v1.products.routes import get_products, delete_product, update_product, create_product, get_product_by_id, search_product