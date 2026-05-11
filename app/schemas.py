from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=128)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=256)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    user_id: str
    username: str


class ValidateResponse(BaseModel):
    user_id: str
    username: str
    valid: bool = True
