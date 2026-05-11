from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.database import health_check_db, init_db
from app.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Auth Service", version="0.1.0", lifespan=lifespan)
app.include_router(auth_router)


@app.get("/health")
async def health():
    ok = await health_check_db()
    if not ok:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "database": "down"},
        )
    return {"status": "ok", "database": "up"}
