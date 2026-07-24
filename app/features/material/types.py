from enum import Enum

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