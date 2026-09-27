from sqlalchemy import delete, select

from app.features.pricing.entities.promotion_condition import (
    PromotionCondition,
)
from app.features.pricing.models.promotion_condition import (
    PromotionConditionTable,
)
from app.infra.db.repositories.base_repository import BaseRepository


class PromotionConditionRepository(
    BaseRepository[
        PromotionCondition,
        PromotionConditionTable,
    ]
):

    async def get_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[PromotionCondition]:

        statement = (
            select(PromotionConditionTable)
            .where(
                PromotionConditionTable.promotion_id
                == promotion_id
            )
            .order_by(
                PromotionConditionTable.created_at.asc(),
            )
        )

        result = await self._db_session.execute(statement)

        return [
            self._base_mapper.to_entity(model)
            for model in result.scalars().all()
        ]

    async def add_all(
        self,
        *,
        entities: list[PromotionCondition],
    ) -> list[PromotionCondition]:

        models = [
            self._base_mapper.to_db_model(entity)
            for entity in entities
        ]

        self._db_session.add_all(models)

        await self._db_session.flush()

        return [
            self._base_mapper.to_entity(model)
            for model in models
        ]

    async def delete_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> None:

        statement = delete(
            PromotionConditionTable
        ).where(
            PromotionConditionTable.promotion_id
            == promotion_id
        )

        await self._db_session.execute(statement)