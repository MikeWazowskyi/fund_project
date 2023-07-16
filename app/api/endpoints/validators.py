from http import HTTPStatus
from typing import Optional, Set

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.base import CharityBase
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicates(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Check names duplicates in database"""

    charity_project = await charity_project_crud.get_id_by_name(
        charity_project_name,
        session,
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> Optional[CharityProject]:
    """Check charity project with id exists"""

    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Проекта с id={charity_project_id} не существует!'
        )
    return charity_project


async def check_update_fields_allowed(
        data: CharityBase,
        allowed_to_edit_fields: Set[str],
):
    """Check fields are allowed to be changed"""
    for field, value in data.dict().items():
        if value and field not in allowed_to_edit_fields:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f'Значение поля "{field}" невозможно изменить!',
            )


async def check_amount_is_not_lower_than_original(
        charity_project_data: CharityProjectUpdate,
        charity_project: CharityProject,

) -> None:
    """Check new full amount is not lower than already invested"""

    if charity_project_data.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=('Нельзя снижать требемую сумму '
                    'ниже уже инвестированной!'),
        )


async def check_charity_project_is_not_fully_invested(
        charity_project: CharityProject,
) -> None:
    """Check charity project is already fully invested"""

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_charity_project_before_edit(
        charity_project_data: CharityProjectUpdate,
        charity_project: CharityProject,
        session: AsyncSession,
        *,
        allowed_to_edit_fields: Set[str],
) -> None:
    """Check charity project before it can be edited"""

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


async def check_charity_project_before_delete(
        charity_project: CharityProject,
):
    """Check charity project before it can be deleted"""

    if charity_project.invested_amount > settings.minimum_investing_sum:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
