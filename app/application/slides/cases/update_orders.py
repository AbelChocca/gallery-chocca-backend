from app.domain.slide.slide_dto import UpdateSlidesOrder

from app.core.exceptions import ValidationError
from app.application.slides.service import SlideService

class UpdateOrdersCase:
    def __init__(
            self,
            slide_service: SlideService
            ):
        self._slide_service = slide_service

    def _validate_orders(self, new_orders: list[int], ids: list[int]) -> None:
        if not new_orders:
            raise ValidationError(
                "'new_orders' musn't be empty",
                {
                    "module": "slides",
                    "case": "update_orders_case",
                    "event": "_validate_orders"
                }
            )

        if len(new_orders) != len(set(new_orders)):
            raise ValidationError(
                "The order of slides cannot be repeated",
                {
                    "module": "slides",
                    "case": "update_orders_case",
                    "event": "_validate_orders"
                }
            )
        
        if len(ids) != len(set(ids)):
            raise ValidationError(
                "Slide ids cannot be repeated",
                {
                    "module": "slides",
                    "case": "update_orders_case",
                    "event": "_validate_orders"
                }
            )

    async def execute(
        self,
        command: UpdateSlidesOrder
    ) -> None:
        if not command.slides:
            return None 
        
        self._validate_orders(command.orders, command.ids)

        await self._slide_service.update_orders(command)