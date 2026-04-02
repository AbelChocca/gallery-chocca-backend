from app.application.dashboard.cases.overview import OverviewCase
from app.api.dependencies.products.service import get_product_service
from app.application.products.service import ProductService
from app.api.dependencies.user.service import get_user_service
from app.application.user.service import UserService
from app.api.dependencies.slides.service import get_slide_service
from app.application.slides.service import SlideService

from fastapi import Depends

def get_overview_case(
        product_service: ProductService = Depends(get_product_service),
        user_service: UserService = Depends(get_user_service),
        slide_service: SlideService = Depends(get_slide_service)
    ) -> OverviewCase:
    return OverviewCase(
        product_service=product_service,
        slide_service=slide_service,
        user_service=user_service
    )