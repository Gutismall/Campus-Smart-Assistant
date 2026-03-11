from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from .shared import get_entity_or_404, delete_entity, update_entity

router = APIRouter()

@router.get("/campuses", response_model=List[schemas.CampusResponse])
def get_campuses(db: Session = Depends(get_db)):
    return db.query(models.Campus).all()

@router.post("/campuses", response_model=schemas.CampusResponse)
def create_campus(campus: schemas.CampusCreate, db: Session = Depends(get_db)):
    new_campus = models.Campus(**campus.model_dump())
    db.add(new_campus)
    db.commit()
    db.refresh(new_campus)
    return new_campus

@router.put("/campuses/{campus_id}", response_model=schemas.CampusResponse)
def update_campus(campus_id: int, campus_req: schemas.CampusCreate, db: Session = Depends(get_db)):
    campus = get_entity_or_404(db, models.Campus, campus_id)
    return update_entity(db, campus, campus_req.model_dump())

@router.delete("/campuses/{campus_id}")
def delete_campus(campus_id: int, db: Session = Depends(get_db)):
    return delete_entity(db, models.Campus, campus_id)
