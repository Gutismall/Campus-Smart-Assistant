from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("campus_buildings.id"), nullable=False)
    room_number = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    available_from = Column(Time, nullable=False)
    available_until = Column(Time, nullable=False)
    
    building = relationship("CampusBuilding", back_populates="rooms")
    tests = relationship("Test", back_populates="room")
