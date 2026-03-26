from app.api.schemas.validator_helpers import max_length_validator, max_file_size_validator
from typing import Annotated, List
from fastapi import UploadFile
from pydantic import WrapValidator

ProductImageType = Annotated[
    List[UploadFile],
    WrapValidator(
        max_length_validator(40),
        max_file_size_validator(5 * 1024 * 1024)
    )
]