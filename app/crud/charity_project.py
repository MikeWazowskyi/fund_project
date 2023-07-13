from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,

    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(
                self.model.id,
            ).where(
                self.model.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


charity_project_crud = CRUDCharityProject(CharityProject)
