from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Test(Base):
    __tablename__ = "tests"
    
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    
    room = relationship("Room", back_populates="tests")
    students = relationship("StudentTest", back_populates="test")
