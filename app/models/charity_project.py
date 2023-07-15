from sqlalchemy import Column, String, Text
from .base import CharityBase


class CharityProject(CharityBase):
    name = Column(String(100), unique=True)
    description = Column(Text)

