from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_role
from app.models.user import User, Role
from app.schemas.user import UserResponse, UserUpdate
from app.services import user as user_service
from app.utils.responses import success_response, paginated_response

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get(
    "",
    summary="List all users",
    description="List all users with optional filtering and pagination. Admin only.",
)
def list_users(
    current_user: Annotated[User, Depends(require_role(Role.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    role: Role | None = None,
    is_active: bool | None = None,
    search: str | None = None,
):
    users, total = user_service.get_users(
        db, page=page, limit=limit, role=role, is_active=is_active, search=search
    )
    return paginated_response(
        data=[UserResponse.model_validate(u).model_dump() for u in users],
        total=total,
        page=page,
        limit=limit,
        message="Users retrieved successfully.",
    )


@router.get(
    "/{user_id}",
    summary="Get user by ID",
    description="Retrieve a specific user's details. Admin only.",
)
def get_user(
    user_id: str,
    current_user: Annotated[User, Depends(require_role(Role.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
):
    user = user_service.get_user_by_id(db, user_id)
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="User retrieved successfully.",
    )


@router.patch(
    "/{user_id}",
    summary="Update user",
    description="Update a user's name, role, or active status. Admin only.",
)
def update_user(
    user_id: str,
    data: UserUpdate,
    current_user: Annotated[User, Depends(require_role(Role.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
):
    user = user_service.update_user(db, user_id, data)
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="User updated successfully.",
    )


@router.delete(
    "/{user_id}",
    summary="Delete user",
    description="Soft delete a user (deactivates and marks as deleted). Admin only.",
)
def delete_user(
    user_id: str,
    current_user: Annotated[User, Depends(require_role(Role.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
):
    user_service.soft_delete_user(db, user_id)
    return success_response(message="User deleted successfully.")
