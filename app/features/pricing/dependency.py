from app.features.pricing.service import PricingService
from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.features.pricing.utils.pricing_calculator import ProductPricingCalculator, get_pricing_calculator
from app.shared.pagination.pagination_service import PaginationService, get_pagination_service

from fastapi import Depends

async def get_pricing_service(
    uow: UnitOfWork = Depends(get_uow),
    pagination_service: PaginationService = Depends(get_pagination_service),
    pricing_calculator: ProductPricingCalculator = Depends(get_pricing_calculator)
) -> PricingService:
    return PricingService(
        pricing_rule_repository=uow.pricing_rules,
        product_pricing_repository=uow.product_pricing,
        product_repository=uow.products,
        pagination_service=pagination_service,
        pricing_calculator=pricing_calculator
    )