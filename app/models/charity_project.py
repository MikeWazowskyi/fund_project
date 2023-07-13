from sqlalchemy import Column, String, Text, Boolean
from .base import CharityBase


class CharityProject(CharityBase):
    name = Column(String(100))
    description = Column(Text)
    fully_invested = Column(Boolean, default=False)
