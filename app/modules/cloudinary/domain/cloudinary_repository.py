from abc import ABC, abstractmethod
from app.shared.dto.cloudinary_dto import CloudinaryImageDTO


class CloudinaryRepository(ABC):
    @abstractmethod
    def upload_image(self, file: str, folder: str) -> CloudinaryImageDTO:
        pass

    @abstractmethod
    def delete_image(self, public_id: str) -> None:
        pass