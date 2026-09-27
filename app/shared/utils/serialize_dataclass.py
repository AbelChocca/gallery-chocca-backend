from dataclasses import asdict
from decimal import Decimal
from enum import Enum
from typing import Any


def serialize_dataclass(object) -> dict[str, Any]:
    data = asdict(object)

    return {
        key: (
            str(value)
            if isinstance(value, Decimal)
            else value.value
            if isinstance(value, Enum)
            else value
        )
        for key, value in data.items()
    }