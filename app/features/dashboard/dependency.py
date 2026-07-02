from fastapi import Depends

from app.features.dashboard.use_cases.get_dashboard_overview import (
    GetDashboardOverviewUseCase,
)
from app.features.products.dependency import get_product_service
from app.features.products.service import ProductService
from app.features.slides.dependency import get_slide_service
from app.features.slides.service import SlideService
from app.features.user.dependency import get_user_service
from app.features.user.service import UserService


def get_dashboard_overview_use_case(
    product_service: ProductService = Depends(get_product_service),
    slide_service: SlideService = Depends(get_slide_service),
    user_service: UserService = Depends(get_user_service),
) -> GetDashboardOverviewUseCase:
    return GetDashboardOverviewUseCase(
        product_service=product_service,
        slide_service=slide_service,
        user_service=user_service,
    )