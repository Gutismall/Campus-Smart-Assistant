from pydantic import BaseModel

class DivisionBase(BaseModel):
    name: str
    campus_id: int

class DivisionCreate(DivisionBase):
    pass

class DivisionResponse(DivisionBase):
    id: int
    class Config:
        from_attributes = True
