from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from .shared import get_entity_or_404, delete_entity, update_entity

router = APIRouter()

@router.get("/students", response_model=List[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, req: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = get_entity_or_404(db, models.Student, student_id)
    return update_entity(db, student, req.model_dump())

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return delete_entity(db, models.Student, student_id)
