from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.services.invest import invest
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationDB, DonationCreate, MyDonationDB

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'user_id', 'invested_amount', 'fully_invested'}
)
async def create_new_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Create new CharityProject model instance by only superusers"""
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
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[MyDonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_by_user(user.id, session)
    return donations
