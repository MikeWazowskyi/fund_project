from typing import List, Callable, Awaitable

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.tags import Tag
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, MyDonationDB
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
    - **comment**: comment to donation (optional)
    - **user_id**: id of donation author
    """
    function.__doc__ += common_params
    return function


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
    },
    tags=[Tag.COMMON_USERS, Tag.CREATE]
)
@set_common_docstring
async def create_new_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Create new donation by only registered users"""
    new_donation = await donation_crud.create(
        donation,
        session,
        user=user,
    )
    await invest(new_donation, charity_project_crud, session)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    tags=[Tag.UNAUTHORIZED, Tag.RETRIEVE],
)
@set_common_docstring
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Get all donations"""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[MyDonationDB],
    response_model_exclude_none=True,
    response_model_exclude={'invested_amount', 'fully_invested'},
    tags=[Tag.COMMON_USERS, Tag.RETRIEVE],
)
@set_common_docstring
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Return all donations made by logged-in user"""
    donations = await donation_crud.get_by_user(user.id, session)
    return donations
