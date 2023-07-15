from typing import Set, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicates(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get_id_by_name(
        charity_project_name,
        session,
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> Optional[CharityProject]:
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Charity project with such id does not exists'
        )
    return charity_project


async def check_update_fields_allowed(data, allowed_to_edit_fields):
    for field, value in data.dict().items():
        if value and field not in allowed_to_edit_fields:
            raise HTTPException(
                status_code=422,
                detail=f'Field "{field}" is not allowed for update',
            )


async def check_amount_is_not_lower_than_original(
        charity_project_data: CharityProjectUpdate,
        charity_project: CharityProject,

) -> None:
    if charity_project_data.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Updated full amount cannot be lower than original',
        )


async def check_charity_project_is_not_fully_invested(
        charity_project: CharityProject,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_charity_project_before_edit(
        charity_project_data: CharityProjectUpdate,
        charity_project: CharityProject,
        session: AsyncSession,
        *,
        allowed_to_edit_fields: Set[str],
):
    await check_charity_project_is_not_fully_invested(
        charity_project
    )
    await check_update_fields_allowed(
        charity_project_data,
        allowed_to_edit_fields,
    )
    if charity_project_data.name is not None:
        await check_name_duplicates(
            charity_project_data.name,
            session,
        )
    if charity_project_data.full_amount is not None:
        await check_amount_is_not_lower_than_original(
            charity_project_data,
            charity_project,
        )
