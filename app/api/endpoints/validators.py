from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_name_duplicates(
        meeting_room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_room_id_by_name(
        meeting_room_name,
        session,
    )
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Meeting room with such name is already exists!'
        )
