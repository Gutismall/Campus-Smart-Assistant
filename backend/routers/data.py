from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List

router = APIRouter(
    prefix="/api/data",
    tags=["system admin data handling"],
)

# Stub endpoints for a System Admin to manage foundational database records 
# (E.g., campuses, divisions, buildings, rooms)

@router.post("/campuses", response_model=schemas.CampusResponse)
def create_campus(campus: schemas.CampusCreate, db: Session = Depends(get_db)):
    # TODO: Add dependency here to verify the current user is a system admin
    new_campus = models.Campus(name=campus.name, address_details=campus.address_details)
    db.add(new_campus)
    db.commit()
    db.refresh(new_campus)
    return new_campus

@router.get("/campuses", response_model=List[schemas.CampusResponse])
def get_all_campuses(db: Session = Depends(get_db)):
    return db.query(models.Campus).all()

@router.post("/buildings", response_model=schemas.CampusBuildingResponse)
def create_building(building: schemas.CampusBuildingCreate, db: Session = Depends(get_db)):
    new_building = models.CampusBuilding(name=building.name, campus_id=building.campus_id)
    db.add(new_building)
    db.commit()
    db.refresh(new_building)
    return new_building
