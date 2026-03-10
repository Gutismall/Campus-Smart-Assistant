from pydantic import BaseModel
from typing import Optional
from datetime import time

class RoomBase(BaseModel):
    building_id: int
    room_number: str
    room_type: Optional[str] = None
    capacity: Optional[int] = None
    is_available: Optional[bool] = True
    available_from: Optional[time] = None
    available_until: Optional[time] = None

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    class Config:
        from_attributes = True
