from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.core.exceptions import ValueNotFound
from app.infra.db.exceptions import DatabaseException

from app.features.pricing.entities.promotion_pricing_rule import (
    PromotionPricingRule,
)

from app.features.pricing.mappers.promotion_pricing_rule_mapper import (
    PromotionPricingRuleMapper,
)

from app.features.pricing.models.promotion_pricing_rule import (
    PromotionPricingRuleTable,
)
from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.mappers.pricing_rule_mapper import PricingRuleMapper

class PromotionPricingRuleRepository:

    def __init__(
        self,
        *,
        db_session: AsyncSession,
    ) -> None:
        self._db_session = db_session

    async def save(
        self,
        *,
        entity: PromotionPricingRule,
    ) -> PromotionPricingRule:

        try:
            statement = select(
                PromotionPricingRuleTable
            ).where(
                PromotionPricingRuleTable.promotion_id
                == entity.promotion_id,
                PromotionPricingRuleTable.pricing_rule_id
                == entity.pricing_rule_id,
            )

            result = await self._db_session.execute(statement)

            existing_model = result.scalar_one_or_none()

            model = PromotionPricingRuleMapper.to_db_model(
                entity=entity,
                existing_model=existing_model,
            )

            self._db_session.add(model)

            await self._db_session.flush()
            await self._db_session.refresh(model)

            return PromotionPricingRuleMapper.to_entity(
                model
            )

        except IntegrityError as exc:
            raise DatabaseException(
                "Integrity constraint violation",
                {
                    "repository": "promotion_pricing_rule",
                    "event": "save",
                    "original_error": str(exc.orig),
                },
            ) from exc

        except SQLAlchemyError as exc:
            raise DatabaseException(
                "Postgres error while saving promotion pricing rule",
                {
                    "repository": "promotion_pricing_rule",
                    "event": "save",
                },
            ) from exc

    async def get(
        self,
        *,
        promotion_id: int,
        pricing_rule_id: int,
    ) -> PromotionPricingRule | None:

        statement = select(
            PromotionPricingRuleTable
        ).where(
            PromotionPricingRuleTable.promotion_id
            == promotion_id,
            PromotionPricingRuleTable.pricing_rule_id
            == pricing_rule_id,
        )

        result = await self._db_session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return PromotionPricingRuleMapper.to_entity(
            model
        )

    async def list_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[PromotionPricingRule]:

        statement = (
            select(PromotionPricingRuleTable)
            .where(
                PromotionPricingRuleTable.promotion_id
                == promotion_id
            )
            .order_by(
                PromotionPricingRuleTable.execution_order.asc(),
                PromotionPricingRuleTable.assigned_at.asc(),
            )
        )

        result = await self._db_session.execute(statement)

        return [
            PromotionPricingRuleMapper.to_entity(model)
            for model in result.scalars().all()
        ]

    async def get_pricing_rules_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[PricingRule]:

        statement = (
            select(PricingRuleTable)
            .join(
                PromotionPricingRuleTable,
                PromotionPricingRuleTable.pricing_rule_id
                == PricingRuleTable.id,
            )
            .where(
                PromotionPricingRuleTable.promotion_id
                == promotion_id
            )
            .order_by(
                PromotionPricingRuleTable.execution_order.asc(),
                PromotionPricingRuleTable.assigned_at.asc(),
            )
        )

        result = await self._db_session.execute(
            statement
        )

        return [
            PricingRuleMapper.to_entity(model)
            for model in result.scalars().all()
        ]

    async def delete(
        self,
        *,
        promotion_id: int,
        pricing_rule_id: int,
    ) -> None:

        relation = await self.get(
            promotion_id=promotion_id,
            pricing_rule_id=pricing_rule_id,
        )

        if relation is None:
            raise ValueNotFound(
                "No se encontro la relacion Promocion <-> Regla de precio.",
                {
                    "promotion_id": promotion_id,
                    "pricing_rule_id": pricing_rule_id,
                },
            )

        statement = delete(
            PromotionPricingRuleTable
        ).where(
            PromotionPricingRuleTable.promotion_id
            == promotion_id,
            PromotionPricingRuleTable.pricing_rule_id
            == pricing_rule_id,
        )

        await self._db_session.execute(statement)

    async def delete_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> None:
        statement = delete(
            PromotionPricingRuleTable
        ).where(
            PromotionPricingRuleTable.promotion_id
            == promotion_id
        )

        await self._db_session.execute(statement)

    async def add_all(
        self,
        *,
        entities: list[PromotionPricingRule],
    ) -> list[PromotionPricingRule]:

        models = [
            PromotionPricingRuleMapper.to_db_model(
                entity=entity,
            )
            for entity in entities
        ]

        self._db_session.add_all(models)

        await self._db_session.flush()

        return [
            PromotionPricingRuleMapper.to_entity(model)
            for model in models
        ]