from app.features.products.service import ProductService
from app.features.slides.service import SlideService
from app.features.user.service import UserService

from app.features.dashboard.types import DashboardOverview

class DashboardService:
    def __init__(
            self,
            product_service: ProductService,
            slide_service: SlideService,
            user_service: UserService
        ):
        self._product_service = product_service
        self._slide_service = slide_service
        self._user_service = user_service

    async def overview(self) -> DashboardOverview:
        products_overview = await self._product_service.overview()
        slides_overview = await self._slide_service.overview()
        users_overview = await self._user_service.overview()

        overview_res: DashboardOverview = {
            "products": products_overview,
            "slides": slides_overview,
            "users": users_overview
        }
        return overview_res
