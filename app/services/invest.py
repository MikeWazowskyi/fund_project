from typing import List

from app.crud.base import CRUDBase
from app.models.base import CharityBase


def invest(
        target: CharityBase,
        sources: List[CharityBase],
):
    """Coroutine to perform investing logic"""
    for source in sources:
        left_to_invest = (source.full_amount - source.invested_amount)
        free_to_invest = (target.full_amount - target.invested_amount)
        amount_to_invest = min(free_to_invest, left_to_invest)
        CRUDBase.close_if_invested(source, amount_to_invest)
        CRUDBase.close_if_invested(target, amount_to_invest)
    return target, sources
