from app.features.dashboard.dto import DashboardOverviewDTO
from app.features.products.product_dto import ProductsOverviewDTO
from app.features.slides.dto import SlidesOverviewDTO
from app.features.user.dto import UsersOverviewDTO

from app.features.products.service import ProductService
from app.features.slides.service import SlideService
from app.features.user.service import UserService


class GetDashboardOverviewUseCase:
    def __init__(
        self,
        product_service: ProductService,
        slide_service: SlideService,
        user_service: UserService,
    ):
        self._product_service = product_service
        self._slide_service = slide_service
        self._user_service = user_service

    async def execute(self) -> DashboardOverviewDTO:

        return DashboardOverviewDTO(
            products=ProductsOverviewDTO(
                total=await self._product_service.count_products(),
                per_category=await self._product_service._count_by_category(),
                recent=await self._product_service._get_last_n(3),
            ),
            slides=SlidesOverviewDTO(
                total=await self._slide_service._count_slides(),
                recent=await self._slide_service._get_last_n_slides(3),
                **await self._slide_service._count_slides_by_active_session(),
            ),
            users=UsersOverviewDTO(
                total=await self._user_service._count_users(),
                per_role=await self._user_service._count_users_per_role(),
                recent=await self._user_service._get_last_n_users(3),
                **await self._user_service._count_users_by_active_session(),
            ),
        )