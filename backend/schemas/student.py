from pydantic import BaseModel, ConfigDict
from typing import Optional

class StudentBase(BaseModel):
    user_id: int
    division_id: Optional[int] = None
    enrollment_year: Optional[int] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
