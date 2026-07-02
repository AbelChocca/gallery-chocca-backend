from app.api.helpers.validators import max_file_size_validator
from typing import Annotated, TypedDict
from fastapi import UploadFile
from pydantic import WrapValidator

SlideImageType = Annotated[
    UploadFile,
    WrapValidator(
        max_file_size_validator(5 * 1024 * 1024)
    )
]

class ActiveAndInactiveSlides(TypedDict):
    active: int
    inactive: int

class SlidesOverview(TypedDict):
    total_slides: int
    sessions_count: ActiveAndInactiveSlides
    last_three_slides: list[dict]