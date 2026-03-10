from pydantic import BaseModel, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    id_number: str
    role: str = "student"  # default to student
    division_id: int | None = None
    division_ids: list[int] | None = None


class RegisterResponse(BaseModel):
    id: int
    email: str
    id_number: str
    message: str

    model_config = ConfigDict(from_attributes=True)
