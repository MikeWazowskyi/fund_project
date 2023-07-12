from sqlalchemy import Column, Integer, DateTime

from app.core.db import Base


class CharityBase(Base):
    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    create_date = Column(DateTime)
    close_date = Column(DateTime)
