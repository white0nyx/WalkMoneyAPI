from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.common.database import async_session_maker
from src.common.repository import SQLAlchemyRepository
from src.subcategory.main.models import SubCategory


class SubCategoryRepository(SQLAlchemyRepository):
    model: type[SubCategory] = SubCategory

    async def find_one(self, subcategory_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == subcategory_id)
            stmt = stmt.options(selectinload(self.model.category))
            res = await session.execute(stmt)
            return res.scalar_one_or_none()