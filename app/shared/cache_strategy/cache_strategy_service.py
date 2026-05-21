from app.core.settings.pydantic_settings import Settings
from typing import Dict, Any, List
from enum import Enum
from dataclasses import dataclass
import json
import hashlib

class OperationEnum(str, Enum):
    by_id = "by_id"
    list = "list"
    related = "related"

@dataclass(frozen=True)
class CacheArgs:
    name: str
    operation: OperationEnum
    values: Dict[str, Any]

class CacheStrategyService:
    def __init__(
            self,
            settings: Settings
            ):
        self._settings = settings

    def _normalize_filters(self, **filters) -> Dict[str, Any]:
        return {
            k: sorted(v) if isinstance(v, list) else v
            for k, v in filters.items()
            if v is not None
        }
    def _filters_hash(self, filters: Dict[str, Any]) -> str:
        normalized_filters = json.dumps(filters, sort_keys=True)
        return hashlib.md5(normalized_filters.encode()).hexdigest()

    def generate_key(
            self, 
            args: CacheArgs
            ) -> str:
        clean_filters: Dict[str, Any] = self._normalize_filters(**args.values)
        filters_hash = self._filters_hash(clean_filters)
        return f"v1:{args.name}:{args.operation.value}:{filters_hash}"
    
    def _validate_name(self, name: str) -> str:
        if not isinstance(name, str):
            return "unknow_name"
        return name

    def operation_by_id(self, name: str, entity_id: int) -> CacheArgs:
        name = self._validate_name(name)
        if not isinstance(entity_id, int):
            raise TypeError("'entity_id' must be an integer")

        return CacheArgs(
            name=name,
            operation=OperationEnum.by_id,
            values={"id": entity_id}
        )

    def operation_list(self, name: str, values: Dict[str, Any]) -> CacheArgs:
        name = self._validate_name(name)
        if not isinstance(values, dict):
            raise TypeError("'values' must be a dict")

        return CacheArgs(
            name=name,
            operation=OperationEnum.list,
            values=values
        )
    
    def operation_related(self, name: str, related_value: str) -> CacheArgs:
        name = self._validate_name(name)

        if not isinstance(related_value, str):
            raise TypeError("'related_value' must be a string")
        
        return CacheArgs(
            name=name,
            operation=OperationEnum.related,
            values={"related_value": related_value}
        )
    
    def determinate_ttl(self, args: CacheArgs) -> int:
        if args.operation == OperationEnum.by_id:
            return self._settings.REDIS_MEDIUM_TTL
        elif args.operation == OperationEnum.related:
            return self._settings.REDIS_SHORT_TTL
        
        values: List[str] = [v for v in args.values.values() if v is not None]
        arg_complexity = len(values)

        if arg_complexity <= 2:
            return self._settings.REDIS_LARGE_TTL
        
        if arg_complexity <= 4:
            return self._settings.REDIS_SHORT_TTL
        
        return self._settings.REDIS_MIN_TTL
    
    def generate_family_key(self, args: CacheArgs) -> str:
        return f"v1:{args.name}:{args.operation.value}:*"
    