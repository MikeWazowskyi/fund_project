from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field

CREATE_DATE = (datetime.now() + timedelta(minutes=10)).isoformat(
    timespec='minutes')
CLOSE_DATE = (datetime.now() + timedelta(days=30)).isoformat(
    timespec='minutes')


class CharityBase(BaseModel):
    full_amount: Optional[int] = Field(None, ge=0)
    invested_amount: Optional[int] = Field(None, ge=0)
    create_date: Optional[datetime] = Field(None, example=CREATE_DATE)
    close_date: Optional[datetime] = Field(None, example=CREATE_DATE)
