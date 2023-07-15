from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationDB, DonationCreate


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> List[DonationDB]:
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user_id
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
