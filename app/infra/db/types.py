from typing import TypeVar, Protocol, Optional
from sqlmodel import SQLModel

class GenericModel(SQLModel):
    id: Optional[int]

class HasID(Protocol):
    id: Optional[int]

M = TypeVar("model_type", bound=GenericModel)
E = TypeVar("entity_type", bound=HasID)