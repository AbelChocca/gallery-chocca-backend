from enum import Enum

class CompanyType(str, Enum):
    OLD_DENIM = "OLD_DENIM"
    CHOCCA = 'CHOCCA'

class MaterialAvailabilityStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    CRITICAL = "CRITICAL"
    OUT_OF_STOCK = "OUT_OF_STOCK"

class UnitType(str, Enum):
    UNIT = "UNIT"
    METER = "METER"
    KILOGRAM = "KILOGRAM"

class MaterialType(str, Enum):
    FABRIC = "FABRIC"
    ACCESSORY = "ACCESSORY"
    BAG = "BAG"
    SUPPLY = "SUPPLY"  

class FiberType(str, Enum):
    COTTON = "COTTON"
    SPANDEX = "SPANDEX"
    POLYESTER = "POLYESTER"
    LINEN = "LINEN"
    NYLON = "NYLON"
    VISCOSE = "VISCOSE"