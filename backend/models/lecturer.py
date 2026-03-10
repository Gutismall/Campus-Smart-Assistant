from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models.lecturer_division import lecturer_division_table

class Lecturer(Base):
    __tablename__ = "lecturers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    office_hours = Column(DateTime,nullable=False)
    
    user = relationship("User", back_populates="lecturer_profile")
    divisions = relationship("Division", secondary=lecturer_division_table, back_populates="lecturers")
