from enum import Enum
from dataclasses import dataclass

class OrderByEnum(str, Enum):
    newest = "newest"
    oldest = "oldest"

@dataclass(frozen=True)
class PaginationResponseDTO:
    total_pages: int
    current_page: int