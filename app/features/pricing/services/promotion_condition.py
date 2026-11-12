from app.features.pricing.entities.promotion_condition import (
    PromotionCondition,
)
from app.features.pricing.repositories.promotion_condition_repository import (
    PromotionConditionRepository,
)
from app.features.pricing.types.promotion_types import (
    PromotionConditionType,
)
from app.features.pricing.dtos.promotion_condition import PromotionConditionAssignment, PromotionConditionParameters


class PromotionConditionService:

    def __init__(
        self,
        *,
        promotion_condition_repository: PromotionConditionRepository,
    ) -> None:
        self._promotion_condition_repository = (
            promotion_condition_repository
        )

    async def create(
        self,
        *,
        promotion_id: int,
        condition_type: PromotionConditionType,
        parameters: PromotionConditionParameters,
        description: str | None = None,
    ) -> PromotionCondition:

        condition = PromotionCondition(
            id=None,
            promotion_id=promotion_id,
            condition_type=condition_type,
            parameters=parameters,
            description=description,
            created_at=None,
        )

        self._validate(
            condition=condition,
        )

        return await self._promotion_condition_repository.save(
            entity=condition,
        )

    async def create_many_for_promotion(
        self,
        *,
        promotion_id: int,
        conditions: list[PromotionConditionAssignment],
    ) -> list[PromotionCondition]:

        entities = [
            PromotionCondition(
                id=None,
                promotion_id=promotion_id,
                condition_type=condition.condition_type,
                parameters=condition.parameters,
                description=condition.description,
                created_at=None,
            )
            for condition in conditions
        ]

        for condition in entities:
            condition.validate()

        return await self._promotion_condition_repository.add_all(
            entities=entities,
        )

    async def replace_for_promotion(
        self,
        *,
        promotion_id: int,
        conditions: list[PromotionConditionAssignment],
    ) -> list[PromotionCondition]:

        entities = [
            PromotionCondition(
                id=None,
                promotion_id=promotion_id,
                condition_type=condition.condition_type,
                parameters=condition.parameters,
                description=condition.description,
                created_at=None,
            )
            for condition in conditions
        ]

        for condition in entities:
            condition.validate()

        await self._promotion_condition_repository.delete_by_promotion(
            promotion_id=promotion_id,
        )

        return await self._promotion_condition_repository.add_all(
            entities=entities,
        )

    async def get_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[PromotionCondition]:

        return await self._promotion_condition_repository.get_by_promotion(
            promotion_id=promotion_id,
        )

    async def delete(
        self,
        *,
        condition_id: int,
    ) -> None:

        await self._promotion_condition_repository.delete_by_id(
            model_id=condition_id,
        )