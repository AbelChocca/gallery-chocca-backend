from app.core.exceptions import ValidationError
from typing import List
from fastapi import UploadFile
from app.core.exceptions import ValidationError

def max_length_validator(max_items: int):
    def validator(value, handler):
        items = handler(value)
        if len(items) > max_items:
            raise ValidationError(
                f"Max {max_items} allowed",
                {
                    "event": "validator/max_length_validator"
                }
            )
        return items
    return validator

def file_bytes_seek(max_size_bytes: int, file: UploadFile, index: int = 0) -> None:
    file.file.seek(0, 2) 
    size = file.file.tell()
    file.file.seek(0)
    if size > max_size_bytes:
        raise ValidationError(
            f"File exceeds max size of {max_size_bytes/(1024*1024)} MB",
            {
                "event": "validator/max_file_size_validator",
                "index": index+1,
                "file_name": file.filename,
                "size": size
            }
        )

def max_file_size_validator(max_size_bytes: int):
    def validator(file: UploadFile):
        file_bytes_seek(max_size_bytes, file)
        return file
    return validator

def max_files_size_validator(max_size_bytes: int):
    def validator(files: List[UploadFile]):
        for i, file in enumerate(files):
            file_bytes_seek(max_size_bytes, file, index=i)
        return files
    return validator