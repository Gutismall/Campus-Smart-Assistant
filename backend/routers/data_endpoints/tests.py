from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from .shared import get_entity_or_404, delete_entity, update_entity

router = APIRouter()

@router.get("/tests", response_model=List[schemas.TestResponse])
def get_tests(db: Session = Depends(get_db)):
    return db.query(models.Test).all()

@router.post("/tests", response_model=schemas.TestResponse)
def create_test(test: schemas.TestCreate, db: Session = Depends(get_db)):
    new_test = models.Test(**test.model_dump())
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test

@router.put("/tests/{test_id}", response_model=schemas.TestResponse)
def update_test(test_id: int, req: schemas.TestCreate, db: Session = Depends(get_db)):
    test = get_entity_or_404(db, models.Test, test_id)
    return update_entity(db, test, req.model_dump())

@router.delete("/tests/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    return delete_entity(db, models.Test, test_id)
