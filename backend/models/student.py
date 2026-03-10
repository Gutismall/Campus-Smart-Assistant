from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    division_id = Column(Integer, ForeignKey("divisions.id"))
    enrollment_year = Column(Integer)
    
    user = relationship("User", back_populates="student_profile")
    division = relationship("Division", back_populates="students")
    tests = relationship("StudentTest", back_populates="student")
