from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core.db import Base


class CharityBase(Base):
    """Abstract sqlalchemy model"""
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            'full_amount >= invested_amount',
        ),
    )
    full_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    invested_amount = Column(Integer, default=0)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def close_if_invested(self, amount_to_invest: int):
        self.invested_amount += amount_to_invest
        if self.full_amount == self.invested_amount:
            self.fully_invested = True
            self.close_date = datetime.now()

    def __repr__(self):
        return (f'<name: {self.name}, '
                f'created: {self.create_date},'
                f'full_amount: {self.full_amount}>')
