from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TestBase(BaseModel):
    course_name: str
    date_time: datetime
    room_id: Optional[int] = None
    lecturer_id: Optional[int] = None

class TestCreate(TestBase):
    pass

class TestResponse(TestBase):
    id: int
    class Config:
        from_attributes = True
