from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from .shared import get_entity_or_404, delete_entity, update_entity
from models.division import Division

router = APIRouter()

@router.get("/lecturers", response_model=List[schemas.LecturerResponse])
def get_lecturers(db: Session = Depends(get_db)):
    return db.query(models.Lecturer).all()

@router.post("/lecturers", response_model=schemas.LecturerResponse)
def create_lecturer(lecturer: schemas.LecturerCreate, db: Session = Depends(get_db)):
    data = lecturer.model_dump()
    div_ids = data.pop("division_ids", [])
    new_lec = models.Lecturer(**data)
    if div_ids:
        new_lec.divisions = db.query(Division).filter(Division.id.in_(div_ids)).all()
    db.add(new_lec)
    db.commit()
    db.refresh(new_lec)
    return new_lec

@router.put("/lecturers/{lecturer_id}", response_model=schemas.LecturerResponse)
def update_lecturer(lecturer_id: int, req: schemas.LecturerCreate, db: Session = Depends(get_db)):
    lec = get_entity_or_404(db, models.Lecturer, lecturer_id)
    data = req.model_dump()
    div_ids = data.pop("division_ids", [])
    
    for key, value in data.items():
        setattr(lec, key, value)
    
    # Update relational divisions mapping
    lec.divisions = db.query(Division).filter(Division.id.in_(div_ids)).all()
    db.commit()
    db.refresh(lec)
    return lec

@router.delete("/lecturers/{lecturer_id}")
def delete_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    return delete_entity(db, models.Lecturer, lecturer_id)
