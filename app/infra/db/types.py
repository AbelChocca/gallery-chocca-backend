from typing import TypeVar, Protocol, Optional
from enum import Enum
from sqlmodel import SQLModel

class GenericModel(SQLModel):
    id: Optional[int]

class HasID(Protocol):
    id: Optional[int]

class InventoryMovementType(Enum):
    RESTOCK = "restock"
    MANUAL_ADJUSTMENT = "manual_adjustment"
    SALE = "sale"
    RETURN = "return"

M = TypeVar("model_type", bound=GenericModel)
E = TypeVar("entity_type", bound=HasID)