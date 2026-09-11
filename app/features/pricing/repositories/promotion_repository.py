from sqlalchemy import select, or_

from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.models.model_promotion import PromotionTable
from app.infra.db.repositories.base_repository import BaseRepository
from app.features.pricing.dtos.promotion_dto import PromotionCandidateCriteria, PromotionProductCandidateDTO
from app.features.pricing.models.promotion_target import PromotionTargetTable
from app.features.pricing.types.promotion_types import PromotionTargetType
from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.models.promotion_pricing_rule import PromotionPricingRuleTable
from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.mappers.pricing_rule_mapper import PricingRuleMapper
from app.features.pricing.mappers.promotion_audience_mapper import (
    PromotionAudienceMapper,
)
from app.features.pricing.mappers.promotion_condition_mapper import (
    PromotionConditionMapper,
)
from app.features.pricing.models.promotion_condition import (
    PromotionConditionTable,
)
from app.features.pricing.models.promotion_audience import (
    PromotionAudienceTable,
)
from app.features.pricing.entities.promotion_condition import (
    PromotionCondition,
)
from app.features.pricing.entities.promotion_audience import PromotionAudience
from app.features.pricing.entities.promotion_target import (
    PromotionTarget,
)

from app.features.pricing.mappers.promotion_target_mapper import (
    PromotionTargetMapper,
)

class PromotionRepository(
    BaseRepository[
        Promotion,
        PromotionTable,
    ]
):

    async def get_by_id_with_details(
        self,
        *,
        promotion_id: int,
    ) -> Promotion | None:
        promotion = (
            await self._get_promotions_with_pricing_rules(
                promotion_ids={promotion_id},
            )
        ).get(promotion_id)

        if promotion is None:
            return None

        audiences = await self._get_promotion_audiences(
            promotion_ids={promotion_id},
        )

        conditions = await self._get_promotion_conditions(
            promotion_ids={promotion_id},
        )

        targets = await self._get_promotion_targets(
            promotion_ids={promotion_id},
        )

        promotion.audiences = audiences.get(
            promotion_id,
            [],
        )

        promotion.conditions = conditions.get(
            promotion_id,
            [],
        )

        promotion.targets = targets.get(
            promotion_id,
            [],
        )

        return promotion

    async def find_candidates(
        self,
        *,
        criteria: PromotionCandidateCriteria,
    ) -> list[PromotionProductCandidateDTO]:

        promotion_ids = await self._find_candidate_promotion_ids(
            criteria=criteria,
        )

        if not promotion_ids:
            return []

        promotions = await self._get_promotions_with_pricing_rules(
            promotion_ids=promotion_ids,
        )

        audiences = await self._get_promotion_audiences(
            promotion_ids=promotion_ids,
        )

        conditions = await self._get_promotion_conditions(
            promotion_ids=promotion_ids,
        )

        targets = await self._get_promotion_targets(
            promotion_ids=promotion_ids,
        )

        for promotion_id, promotion in promotions.items():
            promotion.audiences = audiences.get(
                promotion_id,
                [],
            )

            promotion.conditions = conditions.get(
                promotion_id,
                [],
            )

            promotion.targets = targets.get(
                promotion_id,
                [],
            )

        candidates: list[PromotionProductCandidateDTO] = []

        for promotion_id, promotion in promotions.items():
            for target in promotion.targets:
                product_ids = self._resolve_target_product_ids(
                    target=target,
                    criteria=criteria,
                )

                candidates.extend(
                    PromotionProductCandidateDTO(
                        product_id=product_id,
                        promotion=promotion,
                    )
                    for product_id in product_ids
                )

        return candidates

    async def _find_candidate_promotion_ids(
        self,
        *,
        criteria: PromotionCandidateCriteria,
    ) -> set[int]:

        target_conditions = [
            PromotionTargetTable.target_type
            == PromotionTargetType.ALL,

            (
                PromotionTargetTable.target_type
                == PromotionTargetType.PRODUCT
            )
            & (
                PromotionTargetTable.reference_id.in_(
                    criteria.product_ids
                )
            ),

            (
                PromotionTargetTable.target_type
                == PromotionTargetType.CATEGORY
            )
            & (
                PromotionTargetTable.reference_value.in_(
                    [category.value for category in criteria.categories.values()]
                )
            ),

            (
                PromotionTargetTable.target_type
                == PromotionTargetType.BRAND
            )
            & (
                PromotionTargetTable.reference_value.in_(
                    [brand.value for brand in criteria.brands.values()]
                )
            ),
        ]

        statement = (
            select(PromotionTargetTable.promotion_id)
            .join(
                PromotionTable,
                PromotionTable.id
                == PromotionTargetTable.promotion_id,
            )
            .where(
                PromotionTable.is_active.is_(True),
                PromotionTable.sales_channel
                == criteria.sale_channel,
                or_(*target_conditions),
            )
            .distinct()
        )

        result = await self._db_session.execute(statement)

        return set(result.scalars().all())

    async def _get_promotions_with_pricing_rules(
        self,
        *,
        promotion_ids: set[int],
    ) -> dict[int, Promotion]:

        statement = (
            select(
                PromotionTable,
                PricingRuleTable,
                PromotionPricingRuleTable,
            )
            .join(
                PromotionPricingRuleTable,
                PromotionPricingRuleTable.promotion_id
                == PromotionTable.id,
            )
            .join(
                PricingRuleTable,
                PricingRuleTable.id
                == PromotionPricingRuleTable.pricing_rule_id,
            )
            .where(
                PromotionTable.id.in_(promotion_ids),
            )
            .order_by(
            PromotionPricingRuleTable.execution_order.asc(),
            PromotionPricingRuleTable.assigned_at.asc(),
        )
        )

        result = await self._db_session.execute(statement)

        promotions: dict[int, Promotion] = {}
        pricing_rules_by_promotion: dict[int, dict[int, PricingRule]] = {}

        for (
        promotion_row,
        pricing_rule_row,
        relation_row,
    ) in result.all():

            promotion_id = promotion_row.id

            if promotion_id not in promotions:
                promotions[promotion_id] = (
                    self._base_mapper.to_entity(
                        promotion_row
                    )
                )

                pricing_rules_by_promotion[promotion_id] = {}

            pricing_rule = PricingRuleMapper.to_entity(
                pricing_rule_row
            )

            pricing_rules_by_promotion[promotion_id][
                pricing_rule.id
            ] = pricing_rule

        for promotion_id, promotion in promotions.items():
            promotion.pricing_rules = list(
                pricing_rules_by_promotion[promotion_id].values()
            )

        return promotions

    def _resolve_target_product_ids(
        self,
        *,
        target: PromotionTargetTable,
        criteria: PromotionCandidateCriteria,
    ) -> list[int]:

        if target.target_type == PromotionTargetType.ALL:
            return criteria.product_ids

        if target.target_type == PromotionTargetType.PRODUCT:
            return [
                target.reference_id
            ]

        if target.target_type == PromotionTargetType.CATEGORY:
            return [
                product_id
                for product_id, category in criteria.categories.items()
                if category.value == target.reference_value
            ]

        if target.target_type == PromotionTargetType.BRAND:
            return [
                product_id
                for product_id, brand in criteria.brands.items()
                if brand.value == target.reference_value
            ]

        return []

    async def _get_promotion_targets(
        self,
        *,
        promotion_ids: set[int],
    ) -> dict[int, list[PromotionTarget]]:
        statement = (
            select(PromotionTargetTable)
            .where(
                PromotionTargetTable.promotion_id.in_(
                    promotion_ids
                )
            )
        )

        result = await self._db_session.execute(statement)

        targets_by_promotion: dict[int, list[PromotionTarget]] = {}

        for model in result.scalars().all():
            targets_by_promotion.setdefault(
                model.promotion_id,
                [],
            ).append(
                PromotionTargetMapper.to_entity(model)
            )

        return targets_by_promotion

    async def _get_promotion_audiences(
        self,
        *,
        promotion_ids: set[int],
    ) -> dict[int, list[PromotionAudience]]:
        statement = (
            select(PromotionAudienceTable)
            .where(
                PromotionAudienceTable.promotion_id.in_(
                    promotion_ids
                )
            )
            .order_by(
                PromotionAudienceTable.created_at.asc(),
            )
        )

        result = await self._db_session.execute(statement)

        audiences_by_promotion: dict[
            int,
            list[PromotionAudience],
        ] = {}

        for model in result.scalars().all():
            audience = PromotionAudienceMapper.to_entity(model)

            audiences_by_promotion.setdefault(
                audience.promotion_id,
                [],
            ).append(audience)

        return audiences_by_promotion

    async def _get_promotion_conditions(
        self,
        *,
        promotion_ids: set[int],
    ) -> dict[int, list[PromotionCondition]]:
        statement = (
            select(PromotionConditionTable)
            .where(
                PromotionConditionTable.promotion_id.in_(
                    promotion_ids
                )
            )
            .order_by(
                PromotionConditionTable.created_at.asc(),
            )
        )

        result = await self._db_session.execute(statement)

        conditions_by_promotion: dict[
            int,
            list[PromotionCondition],
        ] = {}

        for model in result.scalars().all():
            condition = PromotionConditionMapper.to_entity(model)

            conditions_by_promotion.setdefault(
                condition.promotion_id,
                [],
            ).append(condition)

        return conditions_by_promotion