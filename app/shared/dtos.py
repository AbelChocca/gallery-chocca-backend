from enum import Enum

class OrderByEnum(str, Enum):
    newest = "newest"
    oldest = "oldest"