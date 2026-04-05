from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User
from app.schemas.user import UserUpdate
from app.utils.exceptions import NotFoundException, BadRequestException


def get_users(
    db: Session,
    page: int = 1,
    limit: int = 20,
    role: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
) -> tuple[list[User], int]:

    query = db.query(User).filter(User.deleted_at.is_(None))

    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                User.name.ilike(search_term),
                User.email.ilike(search_term),
            )
        )

    total = query.count()
    users = (
        query.order_by(User.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return users, total


def get_user_by_id(db: Session, user_id: str) -> User:
    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        .first()
    )

    if not user:
        raise NotFoundException(f"User with ID '{user_id}' not found.")
    return user


def update_user(db: Session, user_id: str, data: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        raise BadRequestException("No fields provided for update.")

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def soft_delete_user(db: Session, user_id: str) -> User:
    user = get_user_by_id(db, user_id)
    user.deleted_at = datetime.now(timezone.utc)
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user
