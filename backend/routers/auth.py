from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from pydantic import BaseModel

from database import get_db
from models.user import User
from schemas.auth import LoginRequest, RegisterRequest, RegisterResponse
from schemas.token import Token
from utils.password import hash_password, verify_password
from utils.jwt import create_student_token, create_lecturer_token, create_admin_token, decode_token

from dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

class VerifyResponse(BaseModel):
    valid: bool
    role: str | None = None
    user_id: int | None = None


@router.get("/verify", response_model=VerifyResponse)
def verify_token(payload: dict = Depends(get_current_user)):
    """
    Verify the JWT token from the Authorization header.
    Returns the decoded role and user_id if valid, raises 401 if invalid/expired.
    """
    return VerifyResponse(
        valid=True, 
        role=payload.get("role"), 
        user_id=int(payload.get("sub")) if payload.get("sub") else None
    )


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Checks that email and id_number are not already taken.
    - Hashes the password with bcrypt before saving.
    """
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    if db.query(User).filter(User.id_number == request.id_number).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this ID number already exists.",
        )

    new_user = User(
        email=request.email,
        id_number=request.id_number,
        hashed_password=hash_password(request.password),
        is_active=True,
        is_system_admin=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RegisterResponse(
        id=new_user.id,
        email=new_user.email,
        id_number=new_user.id_number,
        message="User registered successfully.",
    )


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password.
    Returns a JWT whose role (student / lecturer / admin) reflects the user's access level.
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email.",
        )

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Determine role and issue the appropriate token
    if user.is_system_admin:
        token = create_admin_token(user_id=user.id)
        role = "admin"
    elif user.lecturer_profile:
        token = create_lecturer_token(user_id=user.id, lecturer_id=user.lecturer_profile.id)
        role = "lecturer"
    elif user.student_profile:
        token = create_student_token(user_id=user.id, student_id=user.student_profile.id)
        role = "student"
    else:
        # Registered but no profile assigned yet
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no role assigned. Contact an administrator.",
        )

    return Token(access_token=token, token_type="bearer", role=role)
