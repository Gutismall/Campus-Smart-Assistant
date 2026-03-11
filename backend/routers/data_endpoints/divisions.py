from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from .shared import get_entity_or_404, delete_entity, update_entity

router = APIRouter()

@router.get("/divisions", response_model=List[schemas.DivisionResponse])
def get_divisions(db: Session = Depends(get_db)):
    return db.query(models.Division).all()

@router.post("/divisions", response_model=schemas.DivisionResponse)
def create_division(division: schemas.DivisionCreate, db: Session = Depends(get_db)):
    new_div = models.Division(**division.model_dump())
    db.add(new_div)
    db.commit()
    db.refresh(new_div)
    return new_div

@router.put("/divisions/{division_id}", response_model=schemas.DivisionResponse)
def update_division(division_id: int, division_req: schemas.DivisionCreate, db: Session = Depends(get_db)):
    division = get_entity_or_404(db, models.Division, division_id)
    return update_entity(db, division, division_req.model_dump())

@router.delete("/divisions/{division_id}")
def delete_division(division_id: int, db: Session = Depends(get_db)):
    return delete_entity(db, models.Division, division_id)
