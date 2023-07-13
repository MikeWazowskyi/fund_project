from typing import Optional

from pydantic import Field

from app.schemas.base import CharityBase


class DonationBase(CharityBase):
    comment: Optional[str]


class DonationDB(CharityBase):
    id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    full_amount: int = Field(..., gt=0)


class DonationUpdate(DonationBase):
    pass
