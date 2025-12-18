from pydantic import BaseModel

class ReadImageSchema(BaseModel):
    url: str
    public_id: str