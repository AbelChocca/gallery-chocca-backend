from math import ceil, floor

class PaginationService:
    def get_offset(self, page: int, limit: int) -> int:
        return (page - 1) * limit
    
    def get_total_pages(self, total: int, limit: int) -> int:
        total_pages: int = ceil(total / limit)
        return total_pages
    
    def get_current_page(self, offset: int, limit: int) -> int:
        current_page: int = floor(offset / limit) + 1
        return max(1, current_page)
    
def get_pagination_service() -> PaginationService:
    return PaginationService()