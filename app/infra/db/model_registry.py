# model_registry.py

from app.features.material.models.model_material import MaterialTable, MaterialComponentTable # noqa: F401
from app.features.pricing.models.model_promotion import PromotionTable # noqa: F401
from app.features.pricing.models.coupon import CouponTable # noqa: F401
from app.features.pricing.models.coupon_redemption import CouponRedemptionTable # noqa: F401
from app.features.pricing.models.model_pricing_rule import PricingRuleTable # noqa: F401
from app.features.pricing.models.promotion_audience import PromotionAudienceTable # noqa: F401
from app.features.pricing.models.promotion_condition import PromotionConditionTable # noqa: F401
from app.features.pricing.models.promotion_target import PromotionTargetTable # noqa: F401
from app.features.products.models.model_product import ProductTable, VariantSizeTable, VariantTable # noqa: F401
from app.features.balancing.models.accounts_payable import AccountsPayableTable # noqa: F401
from app.features.balancing.models.inventory_valuation import InventoryValuationTable # noqa: F401
from app.features.balancing.models.accounts_receivable import AccountsReceivableTable # noqa: F401
from app.features.balancing.models.balance_snapshot import BalanceSnapshotTable # noqa: F401
from app.features.balancing.models.financial_debt import FinancialDebtTable # noqa: F401
from app.features.balancing.models.other_current_liability import OtherCurrentLiabilityTable # noqa: F401
from app.features.customer.models.customer import Customer # noqa: F401
from app.infra.db.models.model_user import UserTable # noqa: F401