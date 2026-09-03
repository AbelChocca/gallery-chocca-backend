from enum import Enum

class PromotionStackingMode(str, Enum):
    STACKABLE = "STACKABLE"
    EXCLUSIVE = "EXCLUSIVE"

class PromotionTargetType(str, Enum):
    PRODUCT = "PRODUCT"
    CATEGORY = "CATEGORY"
    BRAND = "BRAND"
    COLLECTION = "COLLECTION"
    ALL = "ALL"

class PromotionAudienceType(str, Enum):
    ALL_CUSTOMERS = "ALL_CUSTOMERS"
    CUSTOMER = "CUSTOMER"
    CUSTOMER_TYPE = "CUSTOMER_TYPE"
    CUSTOMER_GROUP = "CUSTOMER_GROUP"

class PromotionConditionType(str, Enum):
    MINIMUM_ORDER_AMOUNT = "MINIMUM_ORDER_AMOUNT"
    MINIMUM_PRODUCT_QUANTITY = "MINIMUM_PRODUCT_QUANTITY"
    PAYMENT_METHOD = "PAYMENT_METHOD"

class CouponType(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"