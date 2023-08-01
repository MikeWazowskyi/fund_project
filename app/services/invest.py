from typing import List

from app.models.base import CharityBase


def invest(
        target: CharityBase,
        sources: List[CharityBase],
):
    """Coroutine to perform investing logic"""
    invested = []
    for source in sources:
        left_to_invest = (source.full_amount - source.invested_amount)
        free_to_invest = (target.full_amount - target.invested_amount)
        amount_to_invest = min(free_to_invest, left_to_invest)
        if amount_to_invest == 0:
            break
        for participant in sources, target:
            participant.close_if_invested(amount_to_invest)
        invested.append(source)
    return target, invested
