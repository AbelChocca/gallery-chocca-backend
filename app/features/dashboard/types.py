from typing import TypedDict
from app.features.products.types import ProductsOverview
from app.features.slides.types import SlidesOverview
from app.features.user.types import UsersOverview

class DashboardOverview(TypedDict):
    products: ProductsOverview
    slides: SlidesOverview
    users: UsersOverview