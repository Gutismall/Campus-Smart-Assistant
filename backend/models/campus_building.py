from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CampusBuilding(Base):
    __tablename__ = "campus_buildings"
    
    id = Column(Integer, primary_key=True, index=True)
    campus_id = Column(Integer, ForeignKey("campuses.id"), nullable=False)
    name = Column(String, nullable=False)
    
    campus = relationship("Campus", back_populates="buildings")
    rooms = relationship("Room", back_populates="building")
