from dataclasses import dataclass, asdict
from app.features.products.dto.product_dto import ProductsOverviewDTO
from app.features.slides.dto import SlidesOverviewDTO
from app.features.user.dto import UsersOverviewDTO

@dataclass(slots=True)
class DashboardOverviewDTO:
    products: ProductsOverviewDTO
    slides: SlidesOverviewDTO
    users: UsersOverviewDTO

    def dto_to_dict(self) -> dict:
        return asdict(self)