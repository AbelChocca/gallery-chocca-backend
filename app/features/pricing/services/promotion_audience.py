from app.features.pricing.entities.promotion_audience import (
    PromotionAudience,
)
from app.features.pricing.repositories.promotion_audience_repository import (
    PromotionAudienceRepository,
)
from app.features.pricing.types.promotion_types import (
    PromotionAudienceType,
)
from app.features.pricing.dtos.promotion_audience_dto import PromotionAudienceAssignment

class PromotionAudienceService:

    def __init__(
        self,
        *,
        promotion_audience_repository: PromotionAudienceRepository,
    ) -> None:
        self._promotion_audience_repository = (
            promotion_audience_repository
        )

    async def create(
        self,
        *,
        promotion_id: int,
        audience_type: PromotionAudienceType,
        reference_id: int | None = None,
        reference_value: str | None = None,
    ) -> PromotionAudience:

        audience = PromotionAudience(
            id=None,
            promotion_id=promotion_id,
            audience_type=audience_type,
            reference_id=reference_id,
            reference_value=reference_value,
        )

        audience.validate()

        return await self._promotion_audience_repository.save(
            entity=audience,
        )

    async def replace_for_promotion(
        self,
        *,
        promotion_id: int,
        audiences: list[PromotionAudienceAssignment],
    ) -> list[PromotionAudience]:

        entities = [
            PromotionAudience(
                id=None,
                promotion_id=promotion_id,
                audience_type=audience.audience_type,
                reference_id=audience.reference_id,
                reference_value=audience.reference_value,
            )
            for audience in audiences
        ]

        for audience in entities:
            audience.validate()

        await self._promotion_audience_repository.delete_by_promotion(
            promotion_id=promotion_id,
        )

        return await self._promotion_audience_repository.add_all(
            entities=entities,
        )

    async def get_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[PromotionAudience]:

        return await self._promotion_audience_repository.get_by_promotion(
            promotion_id=promotion_id,
        )

    async def create_many_for_promotion(
        self,
        *,
        promotion_id: int,
        audiences: list[PromotionAudienceAssignment],
    ) -> list[PromotionAudience]:

        entities = [
            PromotionAudience(
                id=None,
                promotion_id=promotion_id,
                audience_type=audience.audience_type,
                reference_id=audience.reference_id,
                reference_value=audience.reference_value,
                created_at=None,
            )
            for audience in audiences
        ]

        for audience in entities:
            audience.validate()

        return await self._promotion_audience_repository.add_all(
            entities=entities,
        )

    async def delete(
        self,
        *,
        audience_id: int,
    ) -> None:

        await self._promotion_audience_repository.delete_by_id(
            model_id=audience_id,
        )