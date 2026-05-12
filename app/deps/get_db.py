from app.core.database import SessionLocal

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
