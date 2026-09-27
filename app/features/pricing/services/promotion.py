from datetime import datetime, timezone

from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.repositories.promotion_repository import (
    PromotionRepository,
)
from app.features.pricing.types.promotion_types import (
    PromotionStackingMode,
    PromotionApplicationScope
)
from app.features.sales.types.sale import SaleChannel
from app.shared.pagination.pagination_service import PaginationService
from app.shared.pagination.dto import PaginatedDTO
from app.features.pricing.dtos.promotion_dto import PromotionRowDTO

class PromotionService:

    def __init__(
        self,
        *,
        promotion_repository: PromotionRepository,
        pagination_service: PaginationService
    ) -> None:
        self._promotion_repository = promotion_repository
        self._pagination_service = pagination_service

    async def create(
        self,
        *,
        name: str,
        description: str | None,
        sales_channel: SaleChannel,
        stacking_mode: PromotionStackingMode,
        application_scope: PromotionApplicationScope,
        priority: int,
        starts_at: datetime | None,
        ends_at: datetime | None,
        is_active: bool,
    ) -> Promotion:

        promotion = Promotion(
            id=None,
            name=name,
            description=description,
            sales_channel=sales_channel,
            application_scope=application_scope,
            stacking_mode=stacking_mode,
            priority=priority,
            starts_at=starts_at,
            ends_at=ends_at,
            is_active=is_active,
        )

        promotion.validate()

        return await self._promotion_repository.save(
            entity=promotion,
        )

    async def toggle_status(
        self,
        *,
        promotion_id: int,
    ) -> bool:

        return await self._promotion_repository.toggle_status(
            promotion_id=promotion_id,
        )

    async def get_rows(
        self,
        *,
        page: int,
        limit: int,
        search: str | None = None,
        sales_channel: SaleChannel | None = None,
        application_scope: PromotionApplicationScope | None = None,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
    ) -> PaginatedDTO[PromotionRowDTO]:
        offset = self._pagination_service.get_offset(page, limit)

        items, total_items = (
            await self._promotion_repository.get_rows(
                offset=offset,
                limit=limit,
                search=search,
                sales_channel=sales_channel,
                application_scope=application_scope,
                starts_at=starts_at,
                ends_at=ends_at,
            )
        )

        return PaginatedDTO.create(
            items=items,
            total_items=total_items,
            current_page=self._pagination_service.get_current_page(offset, limit),
            total_pages=self._pagination_service.get_total_pages(total_items, limit)
        )

    async def get_by_id(
        self,
        *,
        promotion_id: int,
    ) -> Promotion:

        promotion = await self._promotion_repository.get_by_id(
            model_id=promotion_id,
        )

        return promotion

    async def update(
        self,
        *,
        promotion_id: int,
        changes: dict,
    ) -> None:

        promotion = await self._promotion_repository.get_by_id(
            model_id=promotion_id,
        )

        for field_name, value in changes.items():
            if value is None:
                continue

            setattr(
                promotion,
                field_name,
                value,
            )

        promotion.updated_at = datetime.now(timezone.utc)

        promotion.validate()

        await self._promotion_repository.save(
            entity=promotion,
        )

    async def delete(
        self,
        *,
        promotion_id: int,
    ) -> None:

        await self._promotion_repository.delete_by_id(
            model_id=promotion_id,
        )