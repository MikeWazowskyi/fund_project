from sqlalchemy import Column, String, Text

from .base import CharityBase


class CharityProject(CharityBase):
    """Charity project sqlalchemy model"""

    name = Column(String(100), unique=True)
    description = Column(Text)

    def __repr__(self):
        return (f'<name: {self.name}, '
                f'created: {self.create_date},'
                f'full_amount: {self.full_amount}>')
