from typing import Optional

from pydantic import Field

from app.schemas.base import CharityBase


class DonationBase(CharityBase):
    """Base donation pydantic schema"""

    comment: Optional[str]


class DonationCreate(DonationBase):
    """Create donation pydantic schema"""

    full_amount: int = Field(..., gt=0)


class MyDonationDB(DonationCreate):
    """Read from DB donation pydantic schema attached to logged-in user"""

    id: int

    class Config:
        orm_mode = True


class DonationDB(MyDonationDB):
    """Read from DB donation pydantic schema"""

    user_id: int


class DonationUpdate(DonationBase):
    """Update donation pydantic schema"""

    pass
