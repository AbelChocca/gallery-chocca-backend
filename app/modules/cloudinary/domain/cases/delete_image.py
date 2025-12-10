from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from typing import Dict

class DeleteImageCase:
    def __init__(
            self,
            repo: CloudinaryRepository
            ):
        self.repo = repo

    def execute(self, public_id: str) -> Dict[str, str]:
        self.repo.delete_image(public_id)
        return {"meesage": "The Image was deleted successfully"}