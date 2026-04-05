from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, require_role
from app.models.user import User, Role
from app.schemas.dashboard import (
    SummaryResponse,
    CategoryBreakdownItem,
    TrendDataPoint,
    RecentActivityItem,
)
from app.services import dashboard as dashboard_service
from app.utils.responses import success_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard Analytics"])


@router.get(
    "/summary",
    summary="Financial summary",
    description="Get overall financial summary including total income, expenses, net balance, and record count. Available to all authenticated users.",
)
def get_summary(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    summary = dashboard_service.get_summary(db)
    return success_response(
        data=summary.model_dump(),
        message="Financial summary retrieved successfully.",
    )


@router.get(
    "/category-breakdown",
    summary="Category breakdown",
    description="Get income and expense totals grouped by category. Available to all authenticated users.",
)
def get_category_breakdown(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    breakdown = dashboard_service.get_category_breakdown(db)
    return success_response(
        data=[item.model_dump(by_alias=True) for item in breakdown],
        message="Category breakdown retrieved successfully.",
    )


@router.get(
    "/trends",
    summary="Monthly trends",
    description="Get monthly income and expense trends. Requires ANALYST or ADMIN role.",
)
def get_trends(
    current_user: Annotated[User, Depends(require_role(Role.ANALYST, Role.ADMIN))],
    db: Annotated[Session, Depends(get_db)],
    months: int = Query(12, ge=1, le=24, description="Number of months to include"),
):
    trends = dashboard_service.get_monthly_trends(db, months=months)
    return success_response(
        data=[point.model_dump() for point in trends],
        message="Monthly trends retrieved successfully.",
    )


@router.get(
    "/recent-activity",
    summary="Recent activity",
    description="Get the most recent financial records. Available to all authenticated users.",
)
def get_recent_activity(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    count: int = Query(
        10, ge=1, le=50, description="Number of recent records to return"
    ),
):
    records = dashboard_service.get_recent_activity(db, count=count)
    return success_response(
        data=[
            RecentActivityItem.model_validate(r).model_dump(by_alias=True)
            for r in records
        ],
        message="Recent activity retrieved successfully.",
    )
