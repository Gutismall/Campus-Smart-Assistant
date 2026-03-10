from pydantic import BaseModel
from typing import Optional

class LecturerBase(BaseModel):
    user_id: int
    division_ids: list[int] = []
    title: Optional[str] = None
    office_hours: Optional[str] = None

class LecturerCreate(LecturerBase):
    pass

class LecturerResponse(LecturerBase):
    id: int
    class Config:
        from_attributes = True
