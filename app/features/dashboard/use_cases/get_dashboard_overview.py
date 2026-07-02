from app.features.dashboard.types import DashboardOverview

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

    async def execute(self) -> DashboardOverview:
        products = {
            "total": await self._product_service._count_products(),
            "per_category": await self._product_service._count_by_category(),
            "recent": await self._product_service._get_last_n(3),
        }

        slides_active = (
            await self._slide_service._count_slides_by_active_session()
        )

        slides = {
            "total": await self._slide_service._count_slides(),
            "recent": await self._slide_service._get_last_n_slides(3),
            **slides_active,
        }

        users_active = (
            await self._user_service._count_users_by_active_session()
        )

        users = {
            "total": await self._user_service._count_users(),
            "per_role": await self._user_service._count_users_per_role(),
            "recent": await self._user_service._get_last_n_users(3),
            **users_active,
        }

        return {
            "products": products,
            "slides": slides,
            "users": users,
        }