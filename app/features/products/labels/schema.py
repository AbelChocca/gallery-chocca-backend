from pydantic import BaseModel

class LabelRequest(BaseModel):
    variant_size_id: int
    quantity: int