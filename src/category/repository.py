from sqlalchemy import select
from src.common.database import async_session_maker
from src.category.models import Category

from src.common.repository import SQLAlchemyRepository

class CategoryRepository(SQLAlchemyRepository):
    model: type[Category] = Category

    async def find_by_name(self, name: str):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.name == name)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def find_active_categories(self):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.is_archived == False)
            res = await session.execute(stmt)
            return res.scalars().all()
