from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass(slots=True)
class PaginationDTO:
    current_page: int
    total_pages: int

@dataclass(slots=True)
class PaginatedDTO(Generic[T]):
    items: list[T]
    total_items: int
    pagination: PaginationDTO

    @classmethod
    def create(
        cls,
        items: list[T],
        total_items: int,
        current_page: int,
        total_pages: int,
    ) -> "PaginatedDTO[T]":
        return cls(
            items=items,
            total_items=total_items,
            pagination=PaginationDTO(
                current_page=current_page,
                total_pages=total_pages,
            ),
        )