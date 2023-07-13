from typing import Optional

from pydantic import Field, validator

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
    fully_invested: bool
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Project name'
    )

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    @validator('description')
    def check_description_is_not_empty(cls, value: str):
        if not value:
            raise ValueError('Description cannot be empty')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Project name'
    )
    description: str = Field()
    full_amount: int = Field(..., ge=0)
