from typing import Callable, Any, List, Dict, Coroutine
from app.core.app_exception import AppException, serialize_exception

class SagaStep:
    """Representa un paso de la saga con su acción y compensación"""
    def __init__(
            self, 
            action: Callable[..., Coroutine[Any, Any, Any]], 
            compensation: Callable[..., Coroutine[Any, Any, Any]] | None, 
            action_name: str, 
            compensation_name: str | None = None,
            action_kwargs: dict | None = None, 
            compensation_kwargs: dict | None = None
        ):
        self.action = action
        self.compensation = compensation
        self.action_kwargs = action_kwargs or {}
        self.compensation_kwargs = compensation_kwargs or {}
        self.compensation_executed = False
        self.action_completed = False
        self.action_name: str = action_name
        self.compensation_name: str = compensation_name

class SagaService:
    """Servicio genérico para manejar mini-sagas y compensaciones seguras"""
    def __init__(self):
        self.steps: List[SagaStep] = []
        self.compensation_errors: List[Dict[str, Any]] = []

    def add_step(
            self, 
            action: Callable[..., Any], 
            action_name: str,
            compensation: Callable[..., Any] | None = None, 
            compensation_name: str | None = None,
            action_kwargs: dict | None = None, 
            compensation_kwargs: dict | None = None
        ) -> None:
        """Registra un paso con su compensación"""
        step = SagaStep(action=action, compensation=compensation, action_name=action_name, compensation_name=compensation_name, action_kwargs=action_kwargs, compensation_kwargs=compensation_kwargs)
        self.steps.append(step)

    async def execute_all(self):
        """Ejecuta todos los pasos de la saga. Si algo falla, corre compensaciones seguras"""
        for i, step in enumerate(self.steps):
            try:
                if not step.action_completed:
                    # Ejecutar acción
                    await step.action(**step.action_kwargs)
                    step.action_completed = True
            except AppException as e:
                # Algo falló → ejecutar compensaciones de los pasos ya completados
                for step in reversed(self.steps[:i]): # i -> failed_index
                    step.compensation_executed = await self._execute_compensation(step)
                # Lanza la excepción original con context de errores de compensación
                raise AppException("Saga failed", {"original_exception": serialize_exception(e), "compensation_errors": self.compensation_errors}) from e
        
    async def execute_last(self) -> Any:
        if not self.steps:
            raise AppException(
                "No steps to execute",
                {
                    "event": "saga_service/execute_last_step"
                }
            )
        try:
            last_step = self.steps[-1]
            return await last_step.action(**last_step.action_kwargs)
        except AppException as ae:
            # Compesate all steps before the last one
            for step in reversed(self.steps[:-1]):
                step.compensation_executed = await self._execute_compensation(step)

            raise AppException(
                "Saga failed", {"original_exception": serialize_exception(ae), "compensation_errors": self.compensation_errors}
            ) from ae
        
    def set_last_step_compensation(
            self, 
            compesation: Callable[..., Coroutine[Any, Any, Any] | Any], 
            compensation_name: str,
            compensation_kwargs: dict
            ) -> None:
        if not self.steps:
            raise AppException(
                "No steps to execute",
                {
                    "event": "saga_service/add_compesate_at_last_step"
                }
            )
        last_step = self.steps[-1]
        last_step.compensation = compesation
        last_step.compensation_name = compensation_name
        last_step.compensation_kwargs = compensation_kwargs

    async def compensate_all(self) -> None:
        if not self.steps:
            return 
        for step in reversed(self.steps):
            step.compensation_executed = await self._execute_compensation(step)

    async def _execute_compensation(self, step: SagaStep) -> bool:
        """Executing compensate on secure mode"""
        try:
            if step.compensation and not step.compensation_executed:
                await step.compensation(**step.compensation_kwargs)
        except AppException as ae:
            # No interrumpe la compensación, solo logea/almacena errores
            self.compensation_errors.append({
                "message": ae.message,
                "action": step.action_name,
                "compensation": step.compensation_name,
                "args": step.args,
                "kwargs": step.kwargs
            })
        return True
    
    def reset(self) -> None:
        self.steps.clear()
        self.compensation_errors.clear()

def get_saga_service() -> SagaService:
    return SagaService()