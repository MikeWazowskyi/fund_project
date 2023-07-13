from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints import validators
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB, \
    CharityProjectCreate

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Create new CharityProject model instance by only superusers"""
    await validators.check_name_duplicates(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session,
    )
    return new_charity_project
