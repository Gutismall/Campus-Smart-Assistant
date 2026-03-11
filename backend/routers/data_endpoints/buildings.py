from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from .shared import get_entity_or_404, delete_entity, update_entity

router = APIRouter()

@router.get("/buildings", response_model=List[schemas.CampusBuildingResponse])
def get_buildings(db: Session = Depends(get_db)):
    return db.query(models.CampusBuilding).all()

@router.post("/buildings", response_model=schemas.CampusBuildingResponse)
def create_building(building: schemas.CampusBuildingCreate, db: Session = Depends(get_db)):
    new_bldg = models.CampusBuilding(**building.model_dump())
    db.add(new_bldg)
    db.commit()
    db.refresh(new_bldg)
    return new_bldg

@router.put("/buildings/{building_id}", response_model=schemas.CampusBuildingResponse)
def update_building(building_id: int, req: schemas.CampusBuildingCreate, db: Session = Depends(get_db)):
    bldg = get_entity_or_404(db, models.CampusBuilding, building_id)
    return update_entity(db, bldg, req.model_dump())

@router.delete("/buildings/{building_id}")
def delete_building(building_id: int, db: Session = Depends(get_db)):
    return delete_entity(db, models.CampusBuilding, building_id)
