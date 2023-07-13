from typing import Optional

from pydantic import Field

from .base import CharityBase


class CharityProjectBase(CharityBase):
    name: Optional[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Project name'
    )
    description: Optional[str]


class CharityProjectDB(CharityProjectBase):
    id: int

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Project name'
    )
    description: str
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectBase):
    pass
