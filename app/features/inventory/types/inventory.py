from enum import Enum

class AvailabilityStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    CRITICAL = "CRITICAL"
    OUT_OF_STOCK = "OUT_OF_STOCK"

class InventoryAnalysisStatus(str, Enum):
    CRITICAL = "critical"
    ATTENTION = "attention"
    HEALTHY = "healthy"
    NO_CONSUMPTION = "no_consumption"