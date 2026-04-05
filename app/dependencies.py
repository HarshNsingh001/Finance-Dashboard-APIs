from typing import Annotated
from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User, Role
from app.utils.security import decode_access_token
from app.utils.exceptions import UnauthorizedException, ForbiddenException


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security_scheme = HTTPBearer()


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(security_scheme)
    ],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise UnauthorizedException("Invalid or expired token.")

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Invalid token payload.")

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if user is None:
        raise UnauthorizedException("User not found.")

    if not user.is_active:
        raise UnauthorizedException("User account is deactivated.")

    return user


def require_role(*allowed_roles: Role):
    def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                f"Role '{current_user.role.value}' is not authorized. "
                f"Required: {', '.join(r.value for r in allowed_roles)}."
            )
        return current_user

    return role_checker
