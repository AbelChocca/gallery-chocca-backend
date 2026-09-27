from app.features.pricing.entities.promotion_target import (
    PromotionTarget,
)
from app.features.pricing.repositories.promotion_target_repository import (
    PromotionTargetRepository,
)
from app.features.pricing.types.promotion_types import (
    PromotionTargetType,
)
from app.features.pricing.dtos.promotion_target import PromotionTargetAssignment


class PromotionTargetService:

    def __init__(
        self,
        *,
        promotion_target_repository: PromotionTargetRepository,
    ) -> None:
        self._promotion_target_repository = (
            promotion_target_repository
        )

    async def get_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[PromotionTarget]:

        return await self._promotion_target_repository.get_by_promotion(
            promotion_id=promotion_id,
        )

    async def create(
        self,
        *,
        promotion_id: int,
        target_type: PromotionTargetType,
        reference_id: int | None = None,
        reference_value: str | None = None,
    ) -> PromotionTarget:

        target = PromotionTarget(
            id=None,
            promotion_id=promotion_id,
            target_type=target_type,
            reference_id=reference_id,
            reference_value=reference_value,
        )

        return await self._promotion_target_repository.save(
            entity=target,
        )

    async def create_many_for_promotion(
        self,
        *,
        promotion_id: int,
        targets: list[PromotionTargetAssignment],
    ) -> list[PromotionTarget]:

        entities = [
            PromotionTarget(
                id=None,
                promotion_id=promotion_id,
                target_type=target.target_type,
                reference_id=target.reference_id,
                reference_value=target.reference_value,
            )
            for target in targets
        ]

        return await self._promotion_target_repository.add_all(
            entities=entities,
        )

    async def replace_for_promotion(
        self,
        *,
        promotion_id: int,
        targets: list[PromotionTargetAssignment],
    ) -> list[PromotionTarget]:

        entities = [
            PromotionTarget(
                id=None,
                promotion_id=promotion_id,
                target_type=target.target_type,
                reference_id=target.reference_id,
                reference_value=target.reference_value,
            )
            for target in targets
        ]

        await self._promotion_target_repository.delete_by_promotion(
            promotion_id=promotion_id,
        )

        return await self._promotion_target_repository.add_all(
            entities=entities,
        )

    async def delete(
        self,
        *,
        target_id: int,
    ) -> None:

        await self._promotion_target_repository.delete_by_id(
            model_id=target_id,
        )