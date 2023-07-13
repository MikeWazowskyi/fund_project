from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from app.core.db import Base


class CharityBase(Base):
    __abstract__ = True
    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    create_date = Column(DateTime, default=datetime.now())
    close_date = Column(DateTime)
