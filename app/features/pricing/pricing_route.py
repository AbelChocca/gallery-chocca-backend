from fastapi import APIRouter

router = APIRouter(prefix='/pricing', tags=['pricing'])

from app.features.pricing.routes import active_pricing_rule, assign_rule_to_multiple_products, assign_rule_to_product, create_pricing_rule, deactivate_pricing_rule, delete_pricing_rule, get_pricing_rule_by_id, get_pricing_rules_by_product_id, get_pricing_rules, get_product_pricing_detail, get_products_pricing_summary, remove_rule_from_product, remove_rule_from_products