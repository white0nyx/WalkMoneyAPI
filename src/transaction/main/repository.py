from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.common.database import async_session_maker
from src.common.repository import SQLAlchemyRepository
from src.transaction.main.models import Transaction
from src.account.main.models import Account

class TransactionRepository(SQLAlchemyRepository):
    model: type[Transaction] = Transaction
    account_model: type[Account] = Account

    async def find_one(self, transaction_id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == transaction_id)
            stmt = stmt.options(selectinload(self.model.account))
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

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

    async def find_all_by_user_id(self, user_id: int):
        async with async_session_maker() as session:

            stmt = select(self.account_model.id).where(self.account_model.user_id == user_id)
            res = await session.execute(stmt)
            accounts_ids = res.scalars().all()

            stmt = select(self.model).where(self.model.account_id.in_(accounts_ids))
            stmt = stmt.order_by(self.model.created_at.desc())
            res = await session.execute(stmt)
            return res.scalars().all()
