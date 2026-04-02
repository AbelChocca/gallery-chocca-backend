from app.application.products.service import ProductService
from app.application.slides.service import SlideService
from app.application.user.service import UserService

# We need to return a payload like these
# class _CategoryCount(BaseModel):
#     total: int
#     category: str

# class _RoleCount(BaseModel):
#     total: int
#     role: str

# class _ProductsOverview(BaseModel):
#     total: int
#     per_category: list[_CategoryCount]
#     recent: list[GridProductRead]

# class _UsersOverview(BaseModel):
#     total: int
#     active: int
#     inactive: int
#     per_role: list[_RoleCount]
#     recent: list[ReadUserSchema]

# class _SlidesOverview(BaseModel):
#     total: int
#     active: int
#     inactive: int
#     recent: list[ReadSlideSchema]

# class OverviewSchema(BaseModel):
#     admin: ReadUserSchema
#     products: _ProductsOverview
#     users: _UsersOverview
#     slides: _SlidesOverview


class OverviewCase:
    def __init__(
            self,
            product_service: ProductService,
            slide_service: SlideService,
            user_service: UserService
            ):
        self._product_service = product_service
        self._slide_service = slide_service
        self._user_service = user_service
    
    async def execute(self) -> dict:
        num_products = await self._product_service.count_products()
        count_products_by_category = await self._product_service.count_by_category()
        last_three_product = await self._product_service.get_last_n(3)

        num_users = await self._user_service.count_users()
        active_and_inactive_users = await self._user_service.count_users_by_active_session()
        count_users_by_role = await self._user_service.count_users_per_role()
        last_three_users = await self._user_service.get_last_n_users(3)

        num_slides = await self._slide_service.count_slides()
        active_and_inactive_slides = await self._slide_service.count_slides_by_active_session()
        last_three_slides = await self._slide_service.get_last_n_slides(3)

        return {
            "products": {
                "total": num_products,
                "per_category": count_products_by_category,
                "recent": last_three_product
            },
            "users": {
                "total": num_users,
                "active": active_and_inactive_users.get("active", 0),
                "inactive": active_and_inactive_users.get("inactive", 0),
                "per_role": count_users_by_role,
                "recent": last_three_users
            },
            "slides": {
                "total": num_slides,
                "active": active_and_inactive_slides.get("active", 0),
                "inactive": active_and_inactive_slides.get("inactive", 0),
                "recent": last_three_slides
            }
        }