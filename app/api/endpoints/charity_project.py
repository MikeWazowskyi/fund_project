from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints import validators
from app.api.endpoints.validators import check_charity_project_before_edit
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB, \
    CharityProjectCreate, CharityProjectUpdate

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
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


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await validators.check_charity_project_exists(
        charity_project_id,
        session
    )
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    # dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        charity_project_data: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    allowed_fields = {'name', 'description', 'full_amount'}
    charity_project = await validators.check_charity_project_exists(
        charity_project_id,
        session,
    )

    await check_charity_project_before_edit(
        charity_project_data,
        charity_project,
        session,
        allowed_to_edit_fields=allowed_fields,
    )

    charity_project = await charity_project_crud.update(
        charity_project,
        charity_project_data,
        session,
    )
    return charity_project
