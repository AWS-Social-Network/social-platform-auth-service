from contextlib import asynccontextmanager

from app.core.database import init_db
from app.api import auth, health

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Auth Service", version="0.1.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(health.router)
