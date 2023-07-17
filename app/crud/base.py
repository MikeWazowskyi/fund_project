from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class with CRUD operations"""

    def __init__(
            self,
            model: Type[ModelType],
    ) -> None:
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        db_object = await session.execute(
            select(
                self.model,
            ).where(
                self.model.id == obj_id
            )
        )
        return db_object.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model),
        )
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            user: Optional[User] = None,
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_invested(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        not_invested_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0
            ).order_by(self.model.create_date)
        )
        return not_invested_objs.scalars().all()

    @staticmethod
    def close_if_invested(obj: ModelType, amount_to_invest: int):
        obj.invested_amount += amount_to_invest
        if obj.full_amount == obj.invested_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()
