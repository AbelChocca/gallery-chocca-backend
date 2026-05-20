from app.features.dashboard.service import DashboardService
from app.features.products.dependency import get_product_service
from app.features.products.service import ProductService
from app.features.slides.service import SlideService
from app.features.slides.dependency import get_slide_service
from app.features.user.dependency import get_user_service
from app.features.user.service import UserService

from fastapi import Depends

def get_dashboard_service(
        product_service: ProductService = Depends(get_product_service),
        slide_service: SlideService = Depends(get_slide_service),
        user_service: UserService = Depends(get_user_service)
        ) -> DashboardService:
    return DashboardService(
        product_service=product_service,
        slide_service=slide_service,
        user_service=user_service
    )