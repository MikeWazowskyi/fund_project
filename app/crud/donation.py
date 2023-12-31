from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate, DonationDB, DonationUpdate


class CRUDDonation(
    CRUDBase[
        Donation,
        DonationCreate,
        DonationUpdate,
    ]
):
    """CRUD class of donation sqlalchemy model"""

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
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
