from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.slide.domain.slide_entity import SlideEntity
from app.modules.slide.domain.dto import SlideFilterDTO

class SlideRepository(ABC):
    """Abstract repository interface for managing SlideEntity persistence.

    This interface defines the required operations for any storage
    implementation (PostgreSQL, SQLite, Redis, in-memory, etc.).
    """

    @abstractmethod
    async def save(self, slide_entity: SlideEntity) -> SlideEntity:
        """Create or update a slide.

        If `slide_entity.id` is None, a new record must be created.
        If `slide_entity.id` has a value, the existing record must be updated.

        Args:
            slide_entity (SlideEntity): The slide to be saved.

        Returns:
            SlideEntity: The saved slide, including its ID if newly created.
        """
        pass

    @abstractmethod
    async def delete_by_id(self, slide_id: int) -> None:
        """Delete a slide by its unique identifier.

        Implementations may choose to silently ignore unknown IDs
        or raise a domain-specific exception.

        Args:
            slide_id (int): Unique slide identifier.

        Returns:
            None
        """
        pass

    @abstractmethod
    async def get_slides_with_filter(
        self,
        slide_filters: SlideFilterDTO,
        offset: int = 0,
        limit: int = 20,
    ) -> List[SlideEntity]:
        """Retrieve slides applying optional filters.

        Filtering options include partial title match, active status,
        creation date, update date, and pagination controls.

        Args:
            offset (int, optional): Starting index for pagination.
            limit (int, optional): Maximum number of results to return.
            titulo_similar (str, optional): Partial title match string.
            activo (bool, optional): Filter by active/inactive status.
            fecha_creada (datetime, optional): Filter by creation date.
            fecha_actualizada (datetime, optional): Filter by last update date.

        Returns:
            List[SlideEntity]: A list of slides that match the filters.
        """
        pass

    @abstractmethod
    async def get_by_id(self, slide_id: int) -> Optional[SlideEntity]:
        """Retrieve a single slide by its ID.

        Args:
            slide_id (int): Unique slide identifier.

        Returns:
            Optional[SlideEntity]: The slide if found, otherwise None.
        """
        pass