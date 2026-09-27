from app.features.pricing.entities.pricing_rule import (
    PricingRule,
)
from app.features.pricing.entities.promotion_pricing_rule import (
    PromotionPricingRule,
)

from app.features.pricing.repositories.pricing_rule_repository import (
    PricingRuleRepository,
)

from app.features.pricing.repositories.promotion_pricing_rule_repository import (
    PromotionPricingRuleRepository,
)

from app.features.pricing.types.pricing_rules_types import (
    PricingRuleType,
)

from app.features.pricing.dtos.pricing_rule_dto import PricingRuleSearchOptionDTO
from app.features.pricing.dtos.promotion_pricing_rule_dto import PromotionPricingRuleAssignment, CreatePromotionPricingRuleAssignment
from app.core.exceptions import ValueNotFound, ValidationError


class PromotionPricingRuleService:

    def __init__(
        self,
        *,
        pricing_rule_repository: PricingRuleRepository,
        promotion_pricing_rule_repository: PromotionPricingRuleRepository,
    ) -> None:
        self._pricing_rule_repository = pricing_rule_repository
        self._promotion_pricing_rule_repository = (
            promotion_pricing_rule_repository
        )

    async def get_by_promotion(
        self,
        *,
        promotion_id: int,
    ) -> list[PricingRule]:

        return (
            await self
            ._promotion_pricing_rule_repository
            .get_pricing_rules_by_promotion(
                promotion_id=promotion_id,
            )
        )

    async def create_and_assign(
        self,
        *,
        promotion_id: int,
        name: str,
        description: str | None,
        type: PricingRuleType,
        parameters: dict,
        execution_order: int,
    ) -> PricingRule:

        rule = PricingRule(
            name=name,
            description=description,
            type=type,
            parameters=parameters,
        )

        rule = await self._pricing_rule_repository.save(
            entity=rule,
        )

        await self.assign_existing(
            promotion_id=promotion_id,
            pricing_rule_id=rule.id,
            execution_order=execution_order,
        )

        return rule

    async def assign_existing(
        self,
        *,
        promotion_id: int,
        pricing_rule_id: int,
        execution_order: int,
    ) -> PromotionPricingRule:

        await self._pricing_rule_repository.get_by_id(
            model_id=pricing_rule_id,
        )

        relation = PromotionPricingRule(
            promotion_id=promotion_id,
            pricing_rule_id=pricing_rule_id,
            execution_order=execution_order,
        )

        relation.validate()

        return await self._promotion_pricing_rule_repository.save(
            entity=relation,
        )

    async def replace_for_promotion(
        self,
        *,
        promotion_id: int,
        rules: list[PromotionPricingRuleAssignment],
    ) -> list[PromotionPricingRule]:

        rule_ids = [
            rule.pricing_rule_id
            for rule in rules
        ]

        existing_rules = await self._pricing_rule_repository.get_by_ids(
            rule_ids=rule_ids,
        )

        existing_ids = {
            rule.id
            for rule in existing_rules
        }

        missing_ids = set(rule_ids) - existing_ids

        if missing_ids:
            raise ValueNotFound(
                "Algunas reglas de precio no fueron encontradas.",
                {
                    "pricing_rule_ids": list(missing_ids),
                },
            )

        await self._promotion_pricing_rule_repository.delete_by_promotion(
            promotion_id=promotion_id,
        )

        relations = [
            PromotionPricingRule(
                promotion_id=promotion_id,
                pricing_rule_id=rule.pricing_rule_id,
                execution_order=rule.execution_order,
            )
            for rule in rules
        ]

        for relation in relations:
            relation.validate()

        return await self._promotion_pricing_rule_repository.add_all(
            entities=relations,
        )

    async def create_many_and_assign(
        self,
        *,
        promotion_id: int,
        rules: list[CreatePromotionPricingRuleAssignment],
    ) -> list[PricingRule]:

        pricing_rules = [
            PricingRule(
                id=None,
                name=rule.name,
                description=rule.description,
                type=rule.type,
                parameters=rule.parameters,
            )
            for rule in rules
        ]

        for pricing_rule in pricing_rules:
            pricing_rule.validate()

        created_rules = (
            await self._pricing_rule_repository.add_all(
                entities=pricing_rules,
            )
        )

        relations: list[PromotionPricingRule] = []

        for pricing_rule, rule in zip(
            created_rules,
            rules,
            strict=True,
        ):
            if pricing_rule.id is None:
                raise ValidationError(
                    "La regla de precio fue creada sin identificador."
                )

            relation = PromotionPricingRule(
                promotion_id=promotion_id,
                pricing_rule_id=pricing_rule.id,
                execution_order=rule.execution_order,
            )

            relation.validate()

            relations.append(relation)

        for relation in relations:
            relation.validate()

        await self._promotion_pricing_rule_repository.add_all(
            entities=relations,
        )

        return created_rules

    async def assign_many_existing(
        self,
        *,
        promotion_id: int,
        rules: list[PromotionPricingRuleAssignment],
    ) -> list[PricingRule]:

        if not rules:
            return []

        rule_ids = [
            rule.pricing_rule_id
            for rule in rules
        ]

        existing_rules = (
            await self._pricing_rule_repository.get_by_ids(
                rule_ids=rule_ids,
            )
        )

        existing_ids = {
            rule.id
            for rule in existing_rules
        }

        missing_ids = (
            set(rule_ids)
            - existing_ids
        )

        if missing_ids:
            raise ValueNotFound(
                "Algunas reglas de precio no fueron encontradas.",
                {
                    "service": "PromotionPricingRuleService",
                    "event": "assign_many_existing",
                    "pricing_rule_ids": list(missing_ids),
                    "promotion_id": promotion_id,
                },
            )

        relations = [
            PromotionPricingRule(
                promotion_id=promotion_id,
                pricing_rule_id=rule.pricing_rule_id,
                execution_order=rule.execution_order,
            )
            for rule in rules
        ]

        for relation in relations:
            relation.validate()

        await self._promotion_pricing_rule_repository.add_all(
            entities=relations,
        )

        return existing_rules

    async def search_options(
        self,
        *,
        search: str | None,
        page: int,
        limit: int,
    ) -> tuple[
        list[PricingRuleSearchOptionDTO],
        int,
    ]:
        offset = (page - 1) * limit

        rules = await self._pricing_rule_repository.search_options(
            search=search,
            offset=offset,
            limit=limit,
        )

        total = await self._pricing_rule_repository.count_search_options(
            search=search,
        )

        return rules, total