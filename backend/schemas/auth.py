from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    id_number: str


class RegisterResponse(BaseModel):
    id: int
    email: str
    id_number: str
    message: str

    class Config:
        from_attributes = True
