from app.shared.services.slug.domain.slug_repository import SlugRepository
from slugify import slugify

class SlugifyRepository(SlugRepository):
    def generate(self, value: str) -> str:
        return slugify(value)
    

def get_slugify_repository() -> SlugRepository:
    return SlugifyRepository()