from app.shared.services.slug.protocol import SlugProtocol
from slugify import slugify

class SlugifyRepository(SlugProtocol):
    def generate(self, value: str) -> str:
        return slugify(value)

def get_slugify_service() -> SlugProtocol:
    return SlugifyRepository()