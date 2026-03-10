from pydantic import BaseModel
from typing import Optional

class StudentTestBase(BaseModel):
    student_id: int
    test_id: int
    is_registered: Optional[bool] = True

class StudentTestCreate(StudentTestBase):
    pass

class StudentTestResponse(StudentTestBase):
    id: int
    class Config:
        from_attributes = True
