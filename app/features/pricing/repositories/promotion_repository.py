from sqlalchemy import select, or_, func, case
from datetime import datetime, timezone

from app.core.exceptions import ValueNotFound
from app.features.pricing.entities.promotion import Promotion
from app.features.pricing.models.model_promotion import PromotionTable
from app.features.pricing.models.promotion_target import PromotionTargetTable
from app.features.pricing.models.coupon import CouponTable
from app.features.pricing.models.promotion_audience import PromotionAudienceTable
from app.features.pricing.models.promotion_condition import PromotionConditionTable
from app.infra.db.repositories.base_repository import BaseRepository
from app.features.pricing.dtos.promotion_dto import PromotionCandidateCriteria, PromotionProductCandidateDTO, PromotionRowDTO
from app.features.pricing.types.promotion_types import PromotionTargetType
from app.features.pricing.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.models.promotion_pricing_rule import PromotionPricingRuleTable
from app.features.pricing.types.promotion_types import PromotionApplicationScope
from app.features.sales.types.sale import SaleChannel
from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.mappers.pricing_rule_mapper import PricingRuleMapper
from app.features.pricing.mappers.promotion_audience_mapper import (
    PromotionAudienceMapper,
)
from app.features.pricing.mappers.promotion_condition_mapper import (
    PromotionConditionMapper,
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

    async def get_rows(
        self,
        *,
        offset: int,
        limit: int,
        search: str | None = None,
        sales_channel: SaleChannel | None = None,
        application_scope: PromotionApplicationScope | None = None,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
    ) -> tuple[list[PromotionRowDTO], int]:

        now = datetime.now(timezone.utc)

        filters = []

        if search is not None and search.strip():
            term = f"%{search.strip()}%"

            filters.append(
                or_(
                    PromotionTable.name.ilike(term),
                    PromotionTable.description.ilike(term),
                )
            )

        if sales_channel is not None:
            filters.append(
                PromotionTable.sales_channel == sales_channel
            )

        if application_scope is not None:
            filters.append(
                PromotionTable.application_scope == application_scope
            )

        if starts_at is not None:
            filters.append(
                PromotionTable.starts_at >= starts_at
            )

        if ends_at is not None:
            filters.append(
                PromotionTable.ends_at <= ends_at
            )

        pricing_rules_count = (
            select(
                func.count(
                    PromotionPricingRuleTable.pricing_rule_id
                )
            )
            .where(
                PromotionPricingRuleTable.promotion_id
                == PromotionTable.id
            )
            .correlate(PromotionTable)
            .scalar_subquery()
        )

        audiences_count = (
            select(
                func.count(PromotionAudienceTable.id)
            )
            .where(
                PromotionAudienceTable.promotion_id
                == PromotionTable.id
            )
            .correlate(PromotionTable)
            .scalar_subquery()
        )

        targets_count = (
            select(
                func.count(PromotionTargetTable.id)
            )
            .where(
                PromotionTargetTable.promotion_id
                == PromotionTable.id
            )
            .correlate(PromotionTable)
            .scalar_subquery()
        )

        conditions_count = (
            select(
                func.count(PromotionConditionTable.id)
            )
            .where(
                PromotionConditionTable.promotion_id
                == PromotionTable.id
            )
            .correlate(PromotionTable)
            .scalar_subquery()
        )

        coupons_count = (
            select(
                func.count(CouponTable.id)
            )
            .where(
                CouponTable.promotion_id
                == PromotionTable.id
            )
            .correlate(PromotionTable)
            .scalar_subquery()
        )

        status_expression = case(
            (
                PromotionTable.is_active.is_(False),
                "INACTIVE",
            ),
            (
                (
                    PromotionTable.starts_at.is_not(None)
                    & (PromotionTable.starts_at > now)
                ),
                "SCHEDULED",
            ),
            (
                (
                    PromotionTable.ends_at.is_not(None)
                    & (PromotionTable.ends_at <= now)
                ),
                "EXPIRED",
            ),
            else_="ACTIVE",
        )

        statement = (
            select(
                PromotionTable.id,
                PromotionTable.name,
                PromotionTable.description,
                PromotionTable.sales_channel,
                PromotionTable.stacking_mode,
                PromotionTable.application_scope,
                PromotionTable.priority,
                PromotionTable.starts_at,
                PromotionTable.ends_at,
                PromotionTable.is_active,
                PromotionTable.created_at,
                PromotionTable.updated_at,
                status_expression.label("status"),
                pricing_rules_count.label(
                    "pricing_rules_count"
                ),
                audiences_count.label(
                    "audiences_count"
                ),
                targets_count.label(
                    "targets_count"
                ),
                conditions_count.label(
                    "conditions_count"
                ),
                coupons_count.label(
                    "coupons_count"
                ),
            )
            .where(*filters)
            .order_by(
                PromotionTable.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        count_statement = select(
            func.count(PromotionTable.id)
        ).where(*filters)

        result = await self._db_session.execute(
            statement
        )

        total_result = await self._db_session.execute(
            count_statement
        )

        rows = result.mappings().all()
        total_items = total_result.scalar_one()

        items = [
            PromotionRowDTO(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                sales_channel=row["sales_channel"],
                stacking_mode=row["stacking_mode"],
                application_scope=row["application_scope"],
                priority=row["priority"],
                starts_at=row["starts_at"],
                ends_at=row["ends_at"],
                is_active=row["is_active"],
                status=row["status"],
                pricing_rules_count=row[
                    "pricing_rules_count"
                ],
                audiences_count=row[
                    "audiences_count"
                ],
                targets_count=row[
                    "targets_count"
                ],
                conditions_count=row[
                    "conditions_count"
                ],
                coupons_count=row[
                    "coupons_count"
                ],
                has_coupon=(
                    row["coupons_count"] > 0
                ),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

        return items, total_items

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

    async def toggle_status(
        self,
        *,
        promotion_id: int,
    ) -> bool:

        promotion = await self._get_model_by_id_non_raise(
            promotion_id
        )

        if not promotion:
            raise ValueNotFound(
                "Promotion not found.",
                {
                    "repository": "postgres_promotion",
                    "event": "toggle_status",
                    "promotion_id": promotion_id,
                },
            )

        promotion.is_active = not promotion.is_active

        await self._db_session.flush()

        return promotion.is_active