from app.features.pricing.dtos.promotion_dto import (
    CreatePromotionDTO,
)
from app.features.pricing.entities.promotion import (
    Promotion,
)

from app.features.pricing.services.promotion import (
    PromotionService,
)
from app.features.pricing.services.promotion_pricing_rule import (
    PromotionPricingRuleService,
    CreatePromotionPricingRuleAssignment
)
from app.features.pricing.services.promotion_audience import (
    PromotionAudienceService,
    PromotionAudienceAssignment,
)
from app.features.pricing.services.promotion_target import (
    PromotionTargetService,
    PromotionTargetAssignment,
)
from app.features.pricing.services.promotion_condition import (
    PromotionConditionService,
    PromotionConditionAssignment,
)
from app.features.pricing.entities.promotion_condition import PromotionCondition
from app.features.pricing.entities.pricing_rule import PricingRule
from app.features.pricing.entities.promotion_target import PromotionTarget
from app.features.pricing.entities.promotion_audience import PromotionAudience
from app.features.pricing.dtos.promotion_pricing_rule_dto import (
    ExistingPromotionPricingRuleDTO, 
    PromotionPricingRuleAssignment, 
    NewPromotionPricingRuleDTO
)

class CreatePromotionUseCase:

    def __init__(
        self,
        *,
        promotion_service: PromotionService,
        promotion_pricing_rule_service: PromotionPricingRuleService,
        promotion_audience_service: PromotionAudienceService,
        promotion_target_service: PromotionTargetService,
        promotion_condition_service: PromotionConditionService,
    ) -> None:

        self._promotion_service = promotion_service

        self._promotion_pricing_rule_service = (
            promotion_pricing_rule_service
        )

        self._promotion_audience_service = (
            promotion_audience_service
        )

        self._promotion_target_service = (
            promotion_target_service
        )

        self._promotion_condition_service = (
            promotion_condition_service
        )

    async def execute(
        self,
        *,
        command: CreatePromotionDTO,
    ) -> Promotion:

        promotion = await self._promotion_service.create(
            name=command.name,
            description=command.description,
            sales_channel=command.sales_channel,
            stacking_mode=command.stacking_mode,
            application_scope=command.application_scope,
            priority=command.priority,
            starts_at=command.starts_at,
            ends_at=command.ends_at,
            is_active=command.is_active,
        )

        promotion.pricing_rules = await self._create_pricing_rules(
            promotion_id=promotion.id,
            command=command,
        )

        promotion.audiences = await self._create_audiences(
            promotion_id=promotion.id,
            command=command,
        )

        promotion.targets = await self._create_targets(
            promotion_id=promotion.id,
            command=command,
        )

        promotion.conditions = await self._create_conditions(
            promotion_id=promotion.id,
            command=command,
        )

        return promotion

    async def _create_pricing_rules(
        self,
        *,
        promotion_id: int,
        command: CreatePromotionDTO,
    ) -> list[PricingRule]:

        new_rules: list[
            CreatePromotionPricingRuleAssignment
        ] = []

        existing_rules: list[
            PromotionPricingRuleAssignment
        ] = []

        for rule in command.pricing_rules:

            if isinstance(
                rule,
                NewPromotionPricingRuleDTO,
            ):
                new_rules.append(
                    CreatePromotionPricingRuleAssignment(
                        name=rule.name,
                        description=rule.description,
                        type=rule.type,
                        parameters=rule.parameters,
                        execution_order=rule.execution_order,
                    )
                )

            elif isinstance(
                rule,
                ExistingPromotionPricingRuleDTO,
            ):
                existing_rules.append(
                    PromotionPricingRuleAssignment(
                        pricing_rule_id=rule.pricing_rule_id,
                        execution_order=rule.execution_order,
                    )
                )

        created_rules = (
            await self._promotion_pricing_rule_service
            .create_many_and_assign(
                promotion_id=promotion_id,
                rules=new_rules,
            )
        )

        assined_rules = (
            await self._promotion_pricing_rule_service
            .assign_many_existing(
                promotion_id=promotion_id,
                rules=existing_rules,
            )
        )

        return [
            *created_rules,
            *assined_rules,
        ]

    async def _create_audiences(
        self,
        *,
        promotion_id: int,
        command: CreatePromotionDTO,
    ) -> list[PromotionAudience]:

        if not command.audiences:
            return []

        audiences = [
            PromotionAudienceAssignment(
                audience_type=audience.audience_type,
                reference_id=audience.reference_id,
                reference_value=audience.reference_value,
            )
            for audience in command.audiences
        ]

        return await self._promotion_audience_service.create_many_for_promotion(
            promotion_id=promotion_id,
            audiences=audiences,
        )

    async def _create_targets(
        self,
        *,
        promotion_id: int,
        command: CreatePromotionDTO,
    ) -> list[PromotionTarget]:

        if not command.targets:
            return []

        targets = [
            PromotionTargetAssignment(
                target_type=target.target_type,
                reference_id=target.reference_id,
                reference_value=target.reference_value,
            )
            for target in command.targets
        ]

        return await self._promotion_target_service.create_many_for_promotion(
            promotion_id=promotion_id,
            targets=targets,
        )

    async def _create_conditions(
        self,
        *,
        promotion_id: int,
        command: CreatePromotionDTO,
    ) -> list[PromotionCondition]:

        if not command.conditions:
            return []

        conditions = [
            PromotionConditionAssignment(
                condition_type=condition.condition_type,
                parameters=condition.parameters,
                description=condition.description,
            )
            for condition in command.conditions
        ]

        return await self._promotion_condition_service.create_many_for_promotion(
            promotion_id=promotion_id,
            conditions=conditions,
        )