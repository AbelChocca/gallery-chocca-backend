from enum import Enum
from typing import TypedDict
from decimal import Decimal

class CartStatus(str, Enum):
    ACTIVE = "active"
    ABANDONED = "abandoned"
    CONVERTED = "converted"