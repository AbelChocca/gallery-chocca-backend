from app.domain.media.protocol import MediaProtocol
from typing import Dict

class DeleteImageCase:
    def __init__(
            self,
            repo: MediaProtocol
            ):
        self.repo = repo

    def execute(self, public_id: str) -> Dict[str, str]:
        self.repo.delete_image(public_id)
        return {"meesage": "The Image was deleted successfully"}