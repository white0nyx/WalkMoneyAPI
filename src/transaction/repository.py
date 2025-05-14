from datetime import datetime

from sqlalchemy import select

from src.common.database import async_session_maker
from src.common.repository import SQLAlchemyRepository
from src.transaction.models import Transaction


class TransactionRepository(SQLAlchemyRepository):
    model: type[Transaction] = Transaction

    async def find_by_account_id(self, account_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.account_id == account_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_by_category_id(self, category_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.category_id == category_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_by_subcategory_id(self, subcategory_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.subcategory_id == subcategory_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_by_date_range(self, start_date: datetime, end_date: datetime):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.transaction_date.between(start_date, end_date))
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_by_transaction_type(self, transaction_type: str):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.transaction_type == transaction_type)
            res = await session.execute(stmt)
            return res.scalars().all()
