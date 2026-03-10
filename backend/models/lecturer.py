from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Lecturer(Base):
    __tablename__ = "lecturers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    division_id = Column(Integer, ForeignKey("divisions.id"))
    title = Column(String)
    office_hours = Column(String)
    
    user = relationship("User", back_populates="lecturer_profile")
    division = relationship("Division", back_populates="lecturers")
    tests = relationship("Test", back_populates="lecturer")
