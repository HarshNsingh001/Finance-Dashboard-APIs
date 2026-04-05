from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.models.record import FinancialRecord
from app.schemas.record import RecordCreate, RecordUpdate
from app.utils.exceptions import NotFoundException, BadRequestException


def create_record(
    db: Session, data: RecordCreate, created_by_id: str
) -> FinancialRecord:
    record = FinancialRecord(
        amount=data.amount,
        type=data.record_type,
        category=data.category,
        date=data.record_date,
        description=data.description,
        created_by_id=created_by_id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_records(
    db: Session,
    page: int = 1,
    limit: int = 20,
    record_type: str | None = None,
    category: str | None = None,
    start_date=None,
    end_date=None,
    search: str | None = None,
    sort_by: str = "date",
    order: str = "desc",
) -> tuple[list[FinancialRecord], int]:
    query = db.query(FinancialRecord).filter(FinancialRecord.deleted_at.is_(None))

    if record_type:
        query = query.filter(FinancialRecord.type == record_type)
    if category:
        query = query.filter(FinancialRecord.category.ilike(f"%{category}%"))
    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)
    if search:
        query = query.filter(FinancialRecord.description.ilike(f"%{search}%"))

    total = query.count()

    # Sorting

    sort_column_map = {
        "date": FinancialRecord.date,
        "amount": FinancialRecord.amount,
        "category": FinancialRecord.category,
        "created_at": FinancialRecord.created_at,
    }
    sort_column = sort_column_map.get(sort_by, FinancialRecord.date)
    order_func = desc if order == "desc" else asc

    records = (
        query.order_by(order_func(sort_column))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return records, total


def get_record_by_id(db: Session, record_id: str) -> FinancialRecord:
    record = (
        db.query(FinancialRecord)
        .filter(
            FinancialRecord.id == record_id,
            FinancialRecord.deleted_at.is_(None),
        )
        .first()
    )

    if not record:
        raise NotFoundException(f"Financial record with ID '{record_id}' not found.")
    return record


def update_record(db: Session, record_id: str, data: RecordUpdate) -> FinancialRecord:

    record = get_record_by_id(db, record_id)

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        raise BadRequestException("No fields provided for update.")

    field_map = {"record_type": "type", "record_date": "date"}
    for field, value in update_data.items():
        orm_field = field_map.get(field, field)
        setattr(record, orm_field, value)

    db.commit()
    db.refresh(record)
    return record


def soft_delete_record(db: Session, record_id: str) -> FinancialRecord:
    record = get_record_by_id(db, record_id)
    record.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(record)
    return record
