from datetime import datetime, timezone

from app.features.pricing.dtos.promotion_dto import (
    CreatePromotionDTO,
)
from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.repositories.promotion_repository import (
    PromotionRepository,
)

class PromotionService:

    def __init__(
        self,
        *,
        promotion_repository: PromotionRepository,
    ) -> None:
        self._promotion_repository = promotion_repository

    async def create(
        self,
        *,
        data: CreatePromotionDTO,
    ) -> Promotion:

        promotion = Promotion(
            id=None,
            name=data.name,
            description=data.description,
            sales_channel=data.sales_channel,
            stacking_mode=data.stacking_mode,
            priority=data.priority,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
            is_active=data.is_active,
        )

        promotion.validate()

        return await self._promotion_repository.save(
            entity=promotion,
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
    ) -> Promotion:

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

        return await self._promotion_repository.save(
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