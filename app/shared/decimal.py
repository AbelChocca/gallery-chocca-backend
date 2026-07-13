from decimal import Decimal
from typing import Annotated
from pydantic import Field

PositiveDecimal = Annotated[
    Decimal,
    Field(ge=0)
]