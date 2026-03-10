from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Campus(Base):
    __tablename__ = "campuses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address_details = Column(String, nullable=False)
    
    divisions = relationship("Division", back_populates="campus")
    buildings = relationship("CampusBuilding", back_populates="campus")
