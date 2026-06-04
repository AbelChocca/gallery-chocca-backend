from app.infra.db.models.model_pricing_rule import PricingRuleTable
from app.features.pricing.entities.pricing_rule import PricingRule
from app.core.exceptions import ValueNotFound

from app.infra.db.repositories.base_repository import BaseRepository
from sqlalchemy import select, and_, func
from sqlmodel import col

class PricingRuleRepository(BaseRepository[PricingRule, PricingRuleTable]):
    async def get_pricing_rule_by_id(self, rule_id: int) -> PricingRule | None:
        return await self.get_by_id(rule_id)
    
    def _build_pricing_rule_conditions(
        self,
        *,
        is_active: bool | None = None,
        type: str | None = None,
        priority_min: int | None = None,
        priority_max: int | None = None,
        search: str | None = None,
    ) -> list:
        
        conditions = []

        if is_active is not None:
            conditions.append(PricingRuleTable.is_active == is_active)

        if type is not None:
            conditions.append(PricingRuleTable.type == type)

        if priority_min is not None:
            conditions.append(PricingRuleTable.priority >= priority_min)

        if priority_max is not None:
            conditions.append(PricingRuleTable.priority <= priority_max)

        if search:
            conditions.append(col(PricingRuleTable.name).ilike(f"%{search}%"))

        return conditions
    
    async def get_pricing_rules(
        self,
        *,
        is_active: bool | None = None,
        type: str | None = None,
        priority_min: int | None = None,
        priority_max: int | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[PricingRule]:

        stmt = select(PricingRuleTable)

        conditions = self._build_pricing_rule_conditions(
            is_active=is_active,
            type=type,
            priority_min=priority_min,
            priority_max=priority_max,
            search=search,
        )

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.limit(limit).offset(offset)

        result = await self._db_session.execute(stmt)
        models = result.scalars().all()

        return [self._base_mapper.to_entity(m) for m in models]
    
    async def count_pricing_rules(
        self,
        *,
        is_active: bool | None = None,
        type: str | None = None,
        priority_min: int | None = None,
        priority_max: int | None = None,
        search: str | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(PricingRuleTable)

        conditions = self._build_pricing_rule_conditions(
            is_active=is_active,
            type=type,
            priority_min=priority_min,
            priority_max=priority_max,
            search=search,
        )

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self._db_session.execute(stmt)

        return result.scalar_one()
        
    async def activate_pricing_rule(
        self,
        rule_id: int
    ) -> None:

        model = await self._get_model_by_id_non_raise(rule_id)

        if not model:
            raise ValueNotFound(
                "Pricing rule not found",
                {"rule_id": rule_id}
            )

        model.is_active = True

    async def deactivate_pricing_rule(
        self,
        rule_id: int
    ) -> None:

        model = await self._get_model_by_id_non_raise(rule_id)

        if not model:
            raise ValueNotFound(
                "Pricing rule not found",
                {"rule_id": rule_id}
            )

        model.is_active = False