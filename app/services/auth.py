from sqlalchemy.orm import Session

from app.models.user import User, Role
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.utils.exceptions import (
    ConflictException,
    UnauthorizedException,
)
from app.config import get_settings

settings = get_settings()


def register_user(db: Session, data: RegisterRequest) -> User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ConflictException(f"A user with email '{data.email}' already exists.")

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=Role.VIEWER,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data: LoginRequest) -> TokenResponse:
    user = (
        db.query(User)
        .filter(
            User.email == data.email,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if not user or not verify_password(data.password, user.hashed_password):
        raise UnauthorizedException("Invalid email or password.")

    if not user.is_active:
        raise UnauthorizedException("User account is deactivated.")

    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
