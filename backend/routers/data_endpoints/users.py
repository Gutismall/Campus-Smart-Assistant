from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from .shared import get_entity_or_404, delete_entity, update_entity
from utils.password import hash_password

router = APIRouter()

@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.is_system_admin == False).all()

@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.is_system_admin:
        raise HTTPException(status_code=403, detail="Cannot create a new system administrator")
        
    new_user = models.User(
        email=user.email,
        id_number=user.id_number,
        password=hash_password(user.password),
        is_system_admin=user.is_system_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_req: schemas.UserCreate, db: Session = Depends(get_db)):
    user = get_entity_or_404(db, models.User, user_id)
    if user.is_system_admin:
        raise HTTPException(status_code=403, detail="Cannot modify a system administrator")
    
    user.email = user_req.email
    user.id_number = user_req.id_number
    if getattr(user_req, 'password', None):
        user.password = hash_password(user_req.password)
    user.is_system_admin = user_req.is_system_admin
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_entity_or_404(db, models.User, user_id)
    if user.is_system_admin:
        raise HTTPException(status_code=403, detail="Cannot delete a system administrator")
    return delete_entity(db, models.User, user_id)
