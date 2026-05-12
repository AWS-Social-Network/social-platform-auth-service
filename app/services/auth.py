from app.repositories import AuthRepo
from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, TokenResponse
from app.models.auth import User
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)


from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, db: AsyncSession):
        self.auth_repo = AuthRepo(db)

    async def register_user(self, register: RegisterRequest) -> RegisterResponse:
        user = await self.auth_repo.get_user_by_email(register.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This Email is already registerd",
            )

        user = await self.auth_repo.get_user_by_username(register.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with the same username already exists",
            )

        user = User(
            username=register.username,
            email=str(register.email),
            hashed_password=hash_password(register.password),
        )

        user = await self.auth_repo.register_user(user)
        return RegisterResponse(user_id=user.id, username=user.username)

    async def login_user(self, request: LoginRequest) -> TokenResponse:
        user = await self.auth_repo.get_user_by_email(request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user found for that email",
            )

        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )

        token = create_access_token({"sub": str(user.id), "username": user.username})
        return TokenResponse(access_token=token)
