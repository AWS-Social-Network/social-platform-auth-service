from pydantic import EmailStr

from app.models.auth import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class AuthRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        result = await self.db.execute(
            select(User).where(
                (User.email == email)
            )
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
