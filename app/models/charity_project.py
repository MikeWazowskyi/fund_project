from sqlalchemy import Column, String, Integer, ForeignKey, Text
from .base import CharityBase


class CharityProject(CharityBase):
    name = Column(String(100))
    description = Column(Text)
