from typing import Awaitable, Callable, List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints import validators
from app.api.endpoints.tags import Tag
from app.api.endpoints.validators import check_charity_project_before_edit
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.invest import invest

router = APIRouter()


def set_common_docstring(function: Callable[..., Awaitable[None]]):
    common_params = """
    - **full_amount**: funds needed to implement the project
    - **fully_invested**: investment status (generates automatically)
    - **invested_amount**: invested funds (generates automatically)
    - **create_date**: start date of project (generates automatically)
    - **close_date**: date when project was invested
    (generates automatically)
    - **name**: name of a project
    - **description**: description of a project
    """
    function.__doc__ += common_params
    return function


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    tags=[Tag.SUPERUSERS, Tag.CREATE]
)
@set_common_docstring
async def create_new_charity_project(
        charity_project: CharityProjectCreate = Body(
            ...,
            examples=CharityProjectCreate.Config.schema_extra['examples']
        ),
        session: AsyncSession = Depends(get_async_session),
):
    """Create new charity project by only superusers"""
    await validators.check_name_duplicates(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session,
    )
    await invest(new_charity_project, donation_crud, session)
    return new_charity_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    tags=[Tag.UNAUTHORIZED, Tag.RETRIEVE],
)
@set_common_docstring
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Get all charity projects"""

    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    tags=[Tag.SUPERUSERS, Tag.REMOVE],
)
@set_common_docstring
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Remove charity project by only superusers"""

    charity_project = await validators.check_charity_project_exists(
        charity_project_id,
        session
    )
    await validators.check_charity_project_before_delete(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    tags=[Tag.SUPERUSERS, Tag.UPDATE],
)
@set_common_docstring
async def partially_update_charity_project(
        charity_project_id: int,
        charity_project_data: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Update charity project by only superusers"""

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
