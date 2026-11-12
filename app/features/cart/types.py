from enum import Enum

class CartStatus(str, Enum):
    ACTIVE = "active"
    ABANDONED = "abandoned"
    CONVERTED = "converted"