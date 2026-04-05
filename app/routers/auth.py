from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services import auth as auth_service
from app.utils.responses import success_response
from app.middleware.rate_limiter import limiter

from starlette.requests import Request

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with VIEWER role by default.",
)
@limiter.limit("10/minute")
def register(
    request: Request,
    data: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
):
    user = auth_service.register_user(db, data)
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="User registered successfully.",
    )


@router.post(
    "/login",
    summary="Login",
    description="Authenticate with email and password to receive a JWT access token.",
)
@limiter.limit("20/minute")
def login(
    request: Request,
    data: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
):
    token = auth_service.login_user(db, data)
    return success_response(
        data=token.model_dump(),
        message="Login successful.",
    )


@router.get(
    "/me",
    summary="Get current user profile",
    description="Returns the profile of the currently authenticated user.",
)
def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return success_response(
        data=UserResponse.model_validate(current_user).model_dump(),
        message="Profile retrieved successfully.",
    )
