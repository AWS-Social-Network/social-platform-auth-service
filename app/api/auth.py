from schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    ValidateResponse,
)

from deps.get_auth import AuthServiceDep
from deps.get_current_user import CurrentUserDep
from fastapi import APIRouter, status

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, auth_service: AuthServiceDep):
    """Registers a new user"""
    return await auth_service.register_user(body)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, auth_service: AuthServiceDep):
    """Checks if user exists, then returns an access token"""
    return await auth_service.login_user(body)


@router.get("/validate", response_model=ValidateResponse)
async def validate_token(current_user: CurrentUserDep):
    """Validates a user's token"""
    return ValidateResponse(user_id=current_user["sub"], username=current_user["username"])
