from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    id_number = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_system_admin = Column(Boolean, default=False)
    
    # Relationships
    student_profile = relationship("Student", uselist=False, back_populates="user", cascade="all, delete-orphan")
    lecturer_profile = relationship("Lecturer", uselist=False, back_populates="user", cascade="all, delete-orphan")
