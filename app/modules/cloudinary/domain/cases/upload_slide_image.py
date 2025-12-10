from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.shared.dto.cloudinary_dto import CloudinaryImageDTO

from typing import IO


class UploadImageCase:
    def __init__(
            self,
            repo: CloudinaryRepository
            ):
        self.repo = repo

    def execute(self, file: IO[bytes], folder: str) -> CloudinaryImageDTO:
        return self.repo.upload_image(file, folder)