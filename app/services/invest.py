from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.base import CharityBase


async def invest(
        obj_to_invest: CharityBase,
        crud_object: CRUDBase,
        session: AsyncSession,
):
    not_invested_objs = await crud_object.get_not_invested(
        session
    )
    try:
        for not_invested_obj in not_invested_objs:
            left_to_invest = (not_invested_obj.full_amount -
                              not_invested_obj.invested_amount)
            free_to_invest = (obj_to_invest.full_amount -
                              obj_to_invest.invested_amount)
            amount_to_invest = min(free_to_invest, left_to_invest)
            close_if_invested(not_invested_obj, amount_to_invest)
            close_if_invested(obj_to_invest, amount_to_invest)

    except Exception:
        await session.rollback()
    else:
        await session.commit()
        await session.refresh(obj_to_invest)


def close_if_invested(model: CharityBase, amount_to_invest: int):
    model.invested_amount += amount_to_invest
    if model.full_amount == model.invested_amount:
        model.fully_invested = True
        model.close_date = datetime.now()
