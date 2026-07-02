from app.infra.saga.saga_service import SagaService

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

        except Exception:
            await self._saga.compensate_all()
            raise