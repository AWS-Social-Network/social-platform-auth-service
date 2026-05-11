from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    ValidateResponse,
)
from app.security import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where((User.email == body.email) | (User.username == body.username))
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email or username already registered")

    user = User(
        username=body.username,
        email=str(body.email),
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return RegisterResponse(user_id=str(user.id), username=user.username)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == str(body.email)))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "username": user.username})
    return TokenResponse(access_token=token)


@router.get("/validate", response_model=ValidateResponse)
async def validate_endpoint(current_user: dict = Depends(get_current_user)):
    return ValidateResponse(user_id=current_user["sub"], username=current_user["username"])
