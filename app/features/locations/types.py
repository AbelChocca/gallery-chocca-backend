from enum import StrEnum

class LocationType(StrEnum):
    STORE = "STORE"
    WORKSHOP = "WORKSHOP"
    WAREHOUSE = "WAREHOUSE"

    CARRIER_PICKUP = "CARRIER_PICKUP"

    OTHER = "OTHER"