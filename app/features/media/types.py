from enum import Enum

class ImageType(str, Enum):
    variant = "variant"
    slide = "slide"
    material = "material"

MAX_IMAGE_SIZE = 5 * 1024 * 1024