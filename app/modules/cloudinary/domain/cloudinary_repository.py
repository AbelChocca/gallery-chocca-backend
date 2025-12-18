from abc import ABC, abstractmethod
from app.modules.cloudinary.domain.dto import CloudinaryImageDTO

from typing import BinaryIO

class CloudinaryRepository(ABC):
    @abstractmethod
    def upload_image(self, file: BinaryIO, folder: str) -> CloudinaryImageDTO:
        pass

    @abstractmethod
    def delete_image(self, public_id: str) -> None:
        pass