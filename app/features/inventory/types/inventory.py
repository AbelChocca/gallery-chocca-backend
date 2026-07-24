from enum import Enum

class AvailabilityStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    CRITICAL = "CRITICAL"
    OUT_OF_STOCK = "OUT_OF_STOCK"