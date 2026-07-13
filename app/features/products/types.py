from app.api.helpers.validators import max_length_validator, max_file_size_validator
from typing import Annotated, List
from fastapi import UploadFile
from pydantic import WrapValidator
from enum import Enum

class ColorFilter(str, Enum):
    black = 'black'
    white = "white"
    gray = "gray"
    brown_beige = "brown_beige"
    blue = "blue"
    green = "green"
    red = "red"

class BrandType(str, Enum):
    BGOO = "BGOO"
    AMD = "AMD"

class CategoryType(str, Enum):
    PANT = 'PANT'
    SHIRT = 'SHIRT'
    SHORT = 'SHORT'
    JACKET = 'JACKET'

class FitType(str, Enum):
    SKINNY = "SKINNY"
    SLIM = "SLIM"
    REGULAR = "REGULAR"
    STRAIGHT = "STRAIGHT"
    RELAXED = "RELAXED"
    LOOSE = "LOOSE"
    MOM_FIT = "MOM_FIT"
    BOOTCUT = "BOOTCUT"
    TAPERED = "TAPERED"
    BOXY = "BOXY"

class SizeType(str, Enum):
    SIZE_28 = "28"
    SIZE_30 = "30"
    SIZE_32 = "32"
    SIZE_34 = "34"
    SIZE_36 = "36"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"

ProductImageType = Annotated[
    List[UploadFile],
    WrapValidator(
        max_length_validator(40),
        max_file_size_validator(5 * 1024 * 1024)
    )
]