from pydantic import BaseModel

class CampusBuildingBase(BaseModel):
    name: str
    campus_id: int

class CampusBuildingCreate(CampusBuildingBase):
    pass

class CampusBuildingResponse(CampusBuildingBase):
    id: int
    class Config:
        from_attributes = True
