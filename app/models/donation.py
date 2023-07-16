from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CharityBase


class Donation(CharityBase):
    """Donation sqlalchemy model"""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (f'<user_id: {self.user_id}, '
                f'created: {self.create_date},'
                f'full_amount: {self.full_amount}>')
