from app.domain.media.protocol import MediaProtocol
from app.domain.media.media_dto import MediaImageDTO

from typing import BinaryIO

class UploadImageCase:
    def __init__(
            self,
            repo: MediaProtocol
            ):
        self.repo = repo

    def execute(self, file: BinaryIO, folder: str) -> MediaImageDTO:
        return self.repo.upload_image(file, folder)