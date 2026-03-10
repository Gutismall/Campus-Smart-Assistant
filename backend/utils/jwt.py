import os
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = os.environ.get("JWT_SECRET", "change-me-in-production")
ALGORITHM = "HS256"
EXPIRE_HOURS = int(os.environ.get("JWT_EXPIRE_HOURS", "24"))


def _make_token(payload: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=EXPIRE_HOURS)
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_student_token(user_id: int, student_id: int) -> str:
    """Create a JWT for a student user."""
    return _make_token({
        "sub": str(user_id),
        "role": "student",
        "student_id": student_id,
    })


def create_lecturer_token(user_id: int, lecturer_id: int) -> str:
    """Create a JWT for a lecturer user."""
    return _make_token({
        "sub": str(user_id),
        "role": "lecturer",
        "lecturer_id": lecturer_id,
    })


def create_admin_token(user_id: int) -> str:
    """Create a JWT for a system admin user."""
    return _make_token({
        "sub": str(user_id),
        "role": "admin",
    })


def decode_token(token: str) -> dict:
    """Decode and verify a JWT. Raises JoseError on failure."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
