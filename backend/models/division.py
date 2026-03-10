from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.lecturer_division import lecturer_division_table

class Division(Base):
    __tablename__ = "divisions"
    
    id = Column(Integer, primary_key=True, index=True)
    campus_id = Column(Integer, ForeignKey("campuses.id"), nullable=False)
    name = Column(String, nullable=False)
    
    campus = relationship("Campus", back_populates="divisions")
    students = relationship("Student", back_populates="division")
    lecturers = relationship("Lecturer", secondary=lecturer_division_table, back_populates="divisions")
