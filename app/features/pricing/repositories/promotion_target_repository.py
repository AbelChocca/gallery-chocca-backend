from sqlalchemy import delete, select

from app.features.pricing.entities.promotion_target import (
    PromotionTarget,
)
from app.features.pricing.models.promotion_target import (
    PromotionTargetTable,
)
from app.infra.db.repositories.base_repository import BaseRepository


class PromotionTargetRepository(
    BaseRepository[
        PromotionTarget,
        PromotionTargetTable,
    ]
):

    async def get_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[PromotionTarget]:

        statement = (
            select(PromotionTargetTable)
            .where(
                PromotionTargetTable.promotion_id
                == promotion_id
            )
            .order_by(
                PromotionTargetTable.created_at.asc(),
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
        entities: list[PromotionTarget],
    ) -> list[PromotionTarget]:

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
            PromotionTargetTable
        ).where(
            PromotionTargetTable.promotion_id
            == promotion_id
        )

        await self._db_session.execute(statement)