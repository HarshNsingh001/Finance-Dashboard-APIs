from datetime import date as DateType
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.record import RecordType


class RecordCreate(BaseModel):

    amount: float = Field(..., gt=0, examples=[1500.00])
    record_type: RecordType = Field(..., alias="type", examples=["INCOME"])
    category: str = Field(..., min_length=1, max_length=100, examples=["Salary"])
    record_date: DateType = Field(..., alias="date", examples=["2024-06-15"])
    description: str | None = Field(
        None,
        max_length=500,
        examples=["Monthly salary payment"],
    )

    model_config = {"populate_by_name": True}


class RecordUpdate(BaseModel):

    amount: float | None = Field(None, gt=0)
    record_type: RecordType | None = Field(None, alias="type")
    category: str | None = Field(None, min_length=1, max_length=100)
    record_date: DateType | None = Field(None, alias="date")
    description: str | None = Field(None, max_length=500)

    model_config = {"populate_by_name": True}


class RecordResponse(BaseModel):

    id: str
    amount: float
    record_type: RecordType = Field(alias="type")
    category: str
    record_date: DateType = Field(alias="date")
    description: str | None
    created_by_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class RecordFilterParams(BaseModel):

    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    record_type: RecordType | None = Field(None, alias="type")
    category: str | None = None
    start_date: DateType | None = None
    end_date: DateType | None = None
    search: str | None = None
    sort_by: str = Field(
        "date",
        pattern="^(date|amount|category|created_at)$",
    )
    order: str = Field("desc", pattern="^(asc|desc)$")

    model_config = {"populate_by_name": True}
