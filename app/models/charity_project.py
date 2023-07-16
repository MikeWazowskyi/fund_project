from sqlalchemy import Column, String, Text
from .base import CharityBase


class CharityProject(CharityBase):
    name = Column(String(100), unique=True)
    description = Column(Text)

    def __repr__(self):
        return (f'<Name: {self.name}, '
                f'created: {self.create_date},'
                f'invested: {self.fully_invested}>')
