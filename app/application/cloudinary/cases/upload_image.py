from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.modules.cloudinary.domain.dto import CloudinaryImageDTO

from typing import BinaryIO


class UploadImageCase:
    def __init__(
            self,
            repo: CloudinaryRepository
            ):
        self.repo = repo

    def execute(self, file: BinaryIO, folder: str) -> CloudinaryImageDTO:
        return self.repo.upload_image(file, folder)