from sqlalchemy import select

from src.budget.models import Budget
from src.common.database import async_session_maker
from src.common.repository import SQLAlchemyRepository

class BudgetRepository(SQLAlchemyRepository):
    model: type[Budget] = Budget

    async def find_by_user_id(self, user_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.user_id == user_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_by_category_id(self, category_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.category_id == category_id)
            res = await session.execute(stmt)
            return res.scalars().all()
