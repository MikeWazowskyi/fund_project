from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate


class CRUDCharityProject(CRUDBase):
    async def create(
            self,
            charity_project: CharityProjectCreate,
            session: AsyncSession,
    ):
        project_data = charity_project.dict()
        project_data['create_date'] = datetime.now()
        charity_project = self.model(**project_data, )
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)
        return charity_project

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
