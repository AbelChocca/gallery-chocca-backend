from pydantic import BaseModel, ConfigDict

class IssuedReceiptResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    external_id: str
    series_number: str

    status: str
    status_description: str

    accepted_by_sunat: bool

    sunat_code: str | None
    sunat_description: str | None

    environment: str | None
    has_fiscal_validity: bool

    remaining_credits: int | None