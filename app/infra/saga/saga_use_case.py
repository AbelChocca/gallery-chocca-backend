from app.infra.saga.saga_service import SagaService
from app.core.exceptions import AppException

class UseCaseSaga:
    def __init__(
        self,
        saga_service: SagaService
    ):
        self._saga = saga_service

    async def execute(
        self,
        operation
    ):
        try:
            return await operation()

        except AppException as ae:

                await self._saga.compensate_all()

                ae.context["compensation_errors"] = (
                    self._saga.compensation_errors
                )

                raise