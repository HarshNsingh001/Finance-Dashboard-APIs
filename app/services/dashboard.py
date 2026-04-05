from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.record import FinancialRecord, RecordType
from app.schemas.dashboard import (
    SummaryResponse,
    CategoryBreakdownItem,
    TrendDataPoint,
)


def get_summary(db: Session) -> SummaryResponse:

    result = (
        db.query(
            func.coalesce(
                func.sum(
                    case(
                        (
                            FinancialRecord.type == RecordType.INCOME,
                            FinancialRecord.amount,
                        )
                    )
                ),
                0.0,
            ).label("total_income"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            FinancialRecord.type == RecordType.EXPENSE,
                            FinancialRecord.amount,
                        )
                    )
                ),
                0.0,
            ).label("total_expenses"),
            func.count(FinancialRecord.id).label("total_records"),
        )
        .filter(
            FinancialRecord.deleted_at.is_(None),
        )
        .first()
    )

    total_income = float(result.total_income)
    total_expenses = float(result.total_expenses)

    return SummaryResponse(
        total_income=round(total_income, 2),
        total_expenses=round(total_expenses, 2),
        net_balance=round(total_income - total_expenses, 2),
        total_records=result.total_records,
    )


def get_category_breakdown(db: Session) -> list[CategoryBreakdownItem]:

    results = (
        db.query(
            FinancialRecord.category,
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label("total"),
            func.count(FinancialRecord.id).label("count"),
        )
        .filter(FinancialRecord.deleted_at.is_(None))
        .group_by(FinancialRecord.category, FinancialRecord.type)
        .order_by(func.sum(FinancialRecord.amount).desc())
        .all()
    )

    return [
        CategoryBreakdownItem(
            category=row.category,
            record_type=row.type,
            total=round(float(row.total), 2),
            count=row.count,
        )
        for row in results
    ]


def get_monthly_trends(db: Session, months: int = 12) -> list[TrendDataPoint]:

    month_label = func.strftime("%Y-%m", FinancialRecord.date)

    results = (
        db.query(
            month_label.label("month"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            FinancialRecord.type == RecordType.INCOME,
                            FinancialRecord.amount,
                        )
                    )
                ),
                0.0,
            ).label("income"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            FinancialRecord.type == RecordType.EXPENSE,
                            FinancialRecord.amount,
                        )
                    )
                ),
                0.0,
            ).label("expenses"),
        )
        .filter(FinancialRecord.deleted_at.is_(None))
        .group_by(month_label)
        .order_by(month_label.desc())
        .limit(months)
        .all()
    )

    results = list(reversed(results))

    return [
        TrendDataPoint(
            month=row.month,
            income=round(float(row.income), 2),
            expenses=round(float(row.expenses), 2),
            net=round(float(row.income) - float(row.expenses), 2),
        )
        for row in results
    ]


def get_recent_activity(db: Session, count: int = 10) -> list[FinancialRecord]:
    return (
        db.query(FinancialRecord)
        .filter(FinancialRecord.deleted_at.is_(None))
        .order_by(FinancialRecord.created_at.desc())
        .limit(count)
        .all()
    )
