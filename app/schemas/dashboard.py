from pydantic import BaseModel, Field
from datetime import date

from app.models.record import RecordType


class SummaryResponse(BaseModel):

    total_income: float
    total_expenses: float
    net_balance: float
    total_records: int


class CategoryBreakdownItem(BaseModel):

    category: str
    record_type: RecordType = Field(alias="type")
    total: float
    count: int

    model_config = {"populate_by_name": True}


class TrendDataPoint(BaseModel):

    month: str
    income: float
    expenses: float
    net: float


class RecentActivityItem(BaseModel):

    id: str
    amount: float
    record_type: RecordType = Field(alias="type")
    category: str
    date: date
    description: str | None
    created_by_id: str

    model_config = {"from_attributes": True, "populate_by_name": True}
