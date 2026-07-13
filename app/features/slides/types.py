from app.api.helpers.validators import max_file_size_validator
from typing import Annotated
from fastapi import UploadFile
from pydantic import WrapValidator

SlideImageType = Annotated[
    UploadFile,
    WrapValidator(
        max_file_size_validator(5 * 1024 * 1024)
    )
]

