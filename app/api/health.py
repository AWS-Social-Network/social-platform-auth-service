from core.database import health_check_db

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health():
    ok = await health_check_db()
    if not ok:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "database": "down"},
        )
    return {"status": "ok", "database": "up"}
