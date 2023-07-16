from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class CharityBase(Base):
    """Abstract sqlalchemy model"""
    __abstract__ = True
    full_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=0)
    create_date = Column(DateTime, default=datetime.now())
    close_date = Column(DateTime)
