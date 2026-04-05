from typing import Annotated
from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User, Role
from app.models.record import RecordType
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.services import record as record_service
from app.utils.responses import success_response, paginated_response

router = APIRouter(prefix="/records", tags=["Financial Records"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a financial record",
    description="Create a new income or expense record. Admin only.",
)
def create_record(
    data: RecordCreate,
    current_user: Annotated[User, Depends(require_role(Role.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
):
    record = record_service.create_record(db, data, created_by_id=current_user.id)
    return success_response(
        data=RecordResponse.model_validate(record).model_dump(by_alias=True),
        message="Financial record created successfully.",
    )


@router.get(
    "",
    summary="List financial records",
    description=(
        "List financial records with filtering, sorting, "
        "and pagination. Available to all authenticated users."
    ),
)
def list_records(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    record_type: RecordType | None = Query(None, alias="type"),
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    search: str | None = None,
    sort_by: str = Query(
        "date",
        pattern="^(date|amount|category|created_at)$",
    ),
    order: str = Query("desc", pattern="^(asc|desc)$"),
):
    records, total = record_service.get_records(
        db,
        page=page,
        limit=limit,
        record_type=record_type,
        category=category,
        start_date=start_date,
        end_date=end_date,
        search=search,
        sort_by=sort_by,
        order=order,
    )
    return paginated_response(
        data=[
            RecordResponse.model_validate(r).model_dump(by_alias=True) for r in records
        ],
        total=total,
        page=page,
        limit=limit,
        message="Financial records retrieved successfully.",
    )


@router.get(
    "/{record_id}",
    summary="Get a financial record",
    description=(
        "Retrieve a specific financial record by ID. "
        "Available to all authenticated users."
    ),
)
def get_record(
    record_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    record = record_service.get_record_by_id(db, record_id)
    return success_response(
        data=RecordResponse.model_validate(record).model_dump(by_alias=True),
        message="Financial record retrieved successfully.",
    )


@router.patch(
    "/{record_id}",
    summary="Update a financial record",
    description="Update fields of a financial record. Admin only.",
)
def update_record(
    record_id: str,
    data: RecordUpdate,
    current_user: Annotated[User, Depends(require_role(Role.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
):
    record = record_service.update_record(db, record_id, data)
    return success_response(
        data=RecordResponse.model_validate(record).model_dump(by_alias=True),
        message="Financial record updated successfully.",
    )


@router.delete(
    "/{record_id}",
    summary="Delete a financial record",
    description="Soft delete a financial record. Admin only.",
)
def delete_record(
    record_id: str,
    current_user: Annotated[User, Depends(require_role(Role.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
):
    record_service.soft_delete_record(db, record_id)
    return success_response(message="Financial record deleted successfully.")
