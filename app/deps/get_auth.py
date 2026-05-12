from typing import Annotated

from deps.get_db import get_db
from services import AuthService

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_auth(db:AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

AuthServiceDep = Annotated[AuthService, Depends(get_db)]
