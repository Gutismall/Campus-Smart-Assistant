from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from .shared import get_entity_or_404, delete_entity, update_entity

router = APIRouter()

@router.get("/rooms", response_model=List[schemas.RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()

@router.post("/rooms", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    new_room = models.Room(**room.model_dump())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def update_room(room_id: int, req: schemas.RoomCreate, db: Session = Depends(get_db)):
    room = get_entity_or_404(db, models.Room, room_id)
    return update_entity(db, room, req.model_dump())

@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return delete_entity(db, models.Room, room_id)
