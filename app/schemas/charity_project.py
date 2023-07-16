from typing import Optional

from pydantic import Field, validator

from .base import CharityBase


class CharityProjectBase(CharityBase):
    """Base charity project pydantic schema"""

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        title='Project name'
    )
    description: Optional[str]


class CharityProjectDB(CharityProjectBase):
    """Read from DB charity project pydantic schema"""

    id: int

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """Update charity project pydantic schema"""

    @validator('description')
    def check_description_is_not_empty(cls, value: str):
        if not value:
            raise ValueError('Description cannot be empty')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    """Create charity project pydantic schema"""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Project name'
    )
    description: str
    full_amount: int = Field(..., gt=0)

    class Config:
        schema_extra = {
            'examples': {
                'valid_request': {
                    'summary': 'Correct data to create project',
                    'description': 'Одиночная фамилия передается строкой',
                    'value': {
                        'name': 'Food for all!',
                        'description': 'Collect funds to feed all cats '
                                       'in the world!',
                        'full_amount': 1000000000000,
                    }
                },
                'invalid_full_amount': {
                    'summary': 'Invalid full amount',
                    'description': 'Full amount must be grater then 0',
                    'value': {
                        'name': 'Food for all!',
                        'description': 'Collect funds to feed all cats '
                                       'in the world!',
                        'full_amount': 0,
                    }
                },
                'invalid_description': {
                    'summary': 'Invalid description',
                    'description': 'Description cannot be empty',
                    'value': {
                        'name': 'Food for all!',
                        'description': '',
                        'full_amount': 1000000000000,
                    }
                },
                'invalid_name': {
                    'summary': 'Invalid name',
                    'description': 'Description cannot be empty',
                    'value': {
                        'name': '',
                        'description': 'Collect funds to feed all cats '
                                       'in the world!',
                        'full_amount': 1000000000000,
                    }
                }
            }
        }
