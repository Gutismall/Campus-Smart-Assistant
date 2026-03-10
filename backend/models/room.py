from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("campus_buildings.id"), nullable=False)
    room_number = Column(String, nullable=False)
    room_type = Column(String)
    capacity = Column(Integer)
    is_available = Column(Boolean, default=True)
    available_from = Column(Time)
    available_until = Column(Time)
    
    building = relationship("CampusBuilding", back_populates="rooms")
    tests = relationship("Test", back_populates="room")
