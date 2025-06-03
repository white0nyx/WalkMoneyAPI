from collections.abc import Sequence

from sqlalchemy import select, Select

from src.category.main.schemas import GetCategoryParamsSchema
from src.common.database import async_session_maker
from src.category.main.models import Category

from src.common.repository import SQLAlchemyRepository

class CategoryRepository(SQLAlchemyRepository):
    model: type[Category] = Category

    async def find_one(self, category_id: int) -> Category | None:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == category_id)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def find_by_name(self, name: str):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.name == name)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def find_all_by_user_id(self, user_id: int, params: GetCategoryParamsSchema) -> Sequence[Category]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.user_id == user_id, self.model.type == params.type)
            stmt = self.apply_pagination(stmt, params)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_all_by_user_id_without_pagination(self, user_id: int, type_: str) -> Sequence[Category]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.user_id == user_id, self.model.type == type_)
            res = await session.execute(stmt)
            return res.scalars().all()
