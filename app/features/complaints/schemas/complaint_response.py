
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.features.complaints.types.complaint_response import (
    ComplaintResponseStatus,
)

class ComplaintResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_id: int

    author_user_id: int | None

    message: str
    status: ComplaintResponseStatus

    recipient_email: str | None
    external_message_id: str | None
    error_message: str | None
    physical_delivery_reference: str | None

    created_at: datetime
    sent_at: datetime | None
    delivered_at: datetime | None

class CreateComplaintResponseRequestSchema(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    message: str = Field(
        min_length=10,
        max_length=10000,
    )

class UpdateComplaintResponseRequestSchema(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    message: str = Field(
        min_length=10,
        max_length=10000,
    )
