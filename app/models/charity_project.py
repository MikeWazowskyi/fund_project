from sqlalchemy import Column, String, Text

from .base import CharityBase


class CharityProject(CharityBase):
    """Charity project sqlalchemy model"""

    name = Column(String(100), unique=True)
    description = Column(Text)


