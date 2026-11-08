from typing import Annotated

from fastapi import Depends, status

from app.features.complaints.complaint_router import (
    router,
)

from app.features.complaints.dependencies.use_cases.create_complaint import (
    get_create_complaint_use_case,
)

from app.features.complaints.use_cases.create_complaint import (
    CreateComplaintUseCase,
)

from app.features.complaints.schemas.complaint import (
    CreateComplaintRequestSchema,
    CreateComplaintResponseSchema,
)

from app.features.complaints.types.complaint import (
    CreateComplaintInput,
)
from app.api.security.rate_limiter.ratelimiter import limiter


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Register a public complaint",
    dependencies=[Depends(limiter.limiter(3, 600))],
    response_model=CreateComplaintResponseSchema,
)
async def create_complaint(
    payload: CreateComplaintRequestSchema,
    case: Annotated[
        CreateComplaintUseCase,
        Depends(get_create_complaint_use_case),
    ],
) -> CreateComplaintResponseSchema:

    result = await case.execute(
        input=CreateComplaintInput(
            **payload.model_dump()
        ),
    )

    return CreateComplaintResponseSchema.model_validate(
        result
    )
