from pydantic import BaseModel
from typing import Optional

class CampusBase(BaseModel):
    name: str
    address_details: Optional[str] = None

class CampusCreate(CampusBase):
    pass

class CampusResponse(CampusBase):
    id: int
    class Config:
        from_attributes = True
