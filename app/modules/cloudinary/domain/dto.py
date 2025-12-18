from dataclasses import dataclass

@dataclass
class CloudinaryImageDTO:
    url: str
    public_id: str